import boto3
import json
import os
import re
import urllib

s3 = boto3.client("s3")

cached_config = None
BUCKET_NAME = os.getenv('bucket_name')

def lambda_handler(event, context):
    record = event["Records"][0]
    input_s3_key = record["s3"]["object"]["key"]  # Example: "processed-json/sample_pdf/split_1.json"
    
    filename_only = os.path.basename(input_s3_key)
    pdf_filename = filename_only.replace("_ocrresults.json", ".pdf")
    ocr_configpath = os.getenv('ocr_configpath')
    cached_config = s3_get_object_Json(BUCKET_NAME,ocr_configpath)
    ocr_resultsfolder = cached_config.get('ocr_resultsfolder')
    ocr_results_suffix = cached_config.get('ocr_results_suffix')
    
    # Extract folder name dynamically (document-specific subfolder)
    folder_name = "/".join(input_s3_key.split("/")[:-1])  # "processed-json/sample_pdf"
    document_name = folder_name.split("/")[-1]  # Extract "sample_pdf"

    ocr_pdf_preprocess_folder = cached_config.get('ocr_pdf_preprocess_folder')
    pdf_file_key = f"{ocr_pdf_preprocess_folder}{document_name}/{pdf_filename}"
    print(f"pdf_filename: {pdf_filename}, pdf_file_key: {pdf_file_key}")
    
    folder_name = urllib.parse.unquote_plus(folder_name)
    pdf_file_key = urllib.parse.unquote_plus(pdf_file_key)
    document_name = urllib.parse.unquote_plus(document_name)
    
    # Retrieve total expected splits from metadata
    metadata = s3.head_object(Bucket=BUCKET_NAME, Key=pdf_file_key)["Metadata"]
    
    total_splits = int(metadata.get("total_p", "1"))
    print(f"total_splits: {total_splits}")
    # List all JSON files in the same document folder
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_name)
    
    json_files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".json")]
    print(f"extracted Parts: {json_files}")

    # Extract part numbers from filenames (e.g., "split_1.json" → 1)
    extracted_parts = sorted(
        [int(re.search(r"_part_(\d+)_ocrresults\.json", key).group(1)) for key in json_files]
    )

    # Check if we have all expected parts
    if len(extracted_parts) == total_splits and sorted(extracted_parts) == list(range(1, total_splits + 1)):
        print(f"All {total_splits} parts received for {document_name}. Merging...")
        merged_json_key = merge_json_files(BUCKET_NAME, folder_name, document_name, ocr_resultsfolder, ocr_results_suffix)
        return {"message": f"Merged JSON stored at {merged_json_key}"}

    return {"message": "Waiting for more JSON files", "received_parts": len(extracted_parts)}

#Merge all splitted files into one single ocr file
def merge_json_files(bucket_name, folder_prefix, document_name,ocr_resultsfolder,ocr_results_suffix):
    """
    Merges extracted JSONs once all splits are available.
    """
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
    print(f"All Splits are available")
    # Get JSON files and sort them based on part number in filename
    json_files = sorted(
        [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".json")],
        key=lambda x: int(re.search(r"_part_(\d+)_ocrresults\.json", x).group(1))
    )
    print(f"Json_file: {json_files}")
   
    
    merged_blocks = []
    page_offset = 0

    for json_file in json_files:
        print(f"Processing: {json_file}")
        obj = s3.get_object(Bucket=bucket_name, Key=json_file)
        textract_data = json.loads(obj["Body"].read().decode("utf-8"))

        blocks = textract_data.get("Blocks", [])
        part_page_count = sum(1 for block in blocks if block["BlockType"] == "PAGE")
        
        
        """
        Optimized code to adjust page numbers and handle relationships efficiently.
        """
    
        # Step 1: Create a dictionary for fast lookups of blocks by "Id"
        block_map = {block["Id"]: block for block in merged_blocks}
    
        # Step 2: Process blocks and adjust page numbers
        for block in blocks:
            # Adjust page numbers for blocks that have a "Page" key
            if "Page" in block:
                block["Page"] += page_offset
    
            # Step 3: Handle relationships for child blocks (key-value pairs, cells in tables)
            if "Relationships" in block:
                for rel in block["Relationships"]:
                    if rel["Type"] == "CHILD":
                        for sub_block_id in rel["Ids"]:
                            # Use the block_map for fast lookup of child blocks
                            merged_block = block_map.get(sub_block_id)
                            if merged_block and "Page" in merged_block:
                                merged_block["Page"] += page_offset
    
            # Append block to merged list
            merged_blocks.append(block)
        
        page_offset += part_page_count

    # Prepare the final merged JSON structure
    merged_json = {
        "DocumentMetadata": {
            "Pages": page_offset
        },
        "Blocks": merged_blocks
    }
    
    # Save merged JSON to S3
    final_json_key = f"{ocr_resultsfolder}{document_name}{ocr_results_suffix}.json"
    print(f"final_json_key: {final_json_key}")
    s3.put_object(Bucket=bucket_name, Key=final_json_key, Body=json.dumps(merged_json))

    print(f"Merged JSON saved to {final_json_key}")
    return final_json_key

def s3_get_object_Json(bucket_name,file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    log_data = json.loads(response['Body'].read().decode('utf-8'))
    return log_data     
    
