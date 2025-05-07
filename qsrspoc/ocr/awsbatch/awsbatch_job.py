import json
import urllib.parse
import time
import os
import re
import sys
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
#initialize Textract client
textract = boto3.client('textract')
s3 = boto3.client('s3')
sns_client = boto3.client('sns')

cached_config = None

def process_textract_job(job_id,bucket_name,s3init_ObjectName,ocr_configpath):
    try:
        #Get Textract document analysis results
        # Parse the message body and extract the job ID
        print(f'job_id: {job_id}, bucket_name: {bucket_name},s3init_ObjectName: {s3init_ObjectName},ocr_configpath: {ocr_configpath}') 
        load_env_from_dockerfile('Dockerfile')
        #Initialize the variables and assign the values
        foldername, filename = s3init_ObjectName.split('/')
        filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
        print('Batch Job started')             
        #Initialize the variables and assign the values
        ###s3init_ObjectName = textract_message['DocumentLocation']['S3ObjectName']
        output_bucket = bucket_name
        foldername, filename = s3init_ObjectName.split('/')
        filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
        
             
        #Get Global variables and Environment variable values 
        cached_config = s3_get_object_Json(output_bucket,ocr_configpath)
        ocrresults_file_suffix = cached_config.get('ocr_results_suffix')
        outputfilename = (f"{filename_without_extension}{ocrresults_file_suffix}")
        cleanpdf_prefix = cached_config.get('cleanpdfprefix')
        clean_outputfilename = (f"{filename_without_extension}_{cleanpdf_prefix}") 
        #ocrresults_folder = os.getenv('ocrresultsfolder')
        ocrresults_folder = cached_config.get('ocr_resultsfolder')
        savecleanpdfs3_featureflag = cached_config.get('savecleanpdfs3')
        topic_arn = os.getenv('topicarn')
        #enable_structured_data = os.getenv('enable_convert_ocr_jsondata_structured')
        enable_structured_data = cached_config.get('enable_convert_ocr_jsondata_structured')
        #enable_simple_text_file = os.getenv('enable_convert_ocr_jsondata_simple')
        enable_simple_text_file = cached_config.get('enable_convert_ocr_jsondata_simple')
        #send_to_batch = os.getenv('send_to_batch')
        send_to_batch = cached_config.get('send_to_batch')
        
        # Check if the job completed successfully and store Json file in S3
        
        # Call Textract to get the job results
        all_results = get_all_results(job_id)
        #Merge all the results in one Json file
        result_json = merge_results(all_results)
        
        # Define the S3 bucket and object key for storing results
        
        output_key = f'{ocrresults_folder}{outputfilename}.json'
        #Add Job_id into metadata of the json file that will be stored in S3
        metadata = {'AWS Textract jobid': f'{job_id}'}
        
        # Upload the AWS TExtract json output results to S3 
        s3_put_object(output_bucket,output_key,result_json,metadata)
        
        #If the json data needed to convert into structured text file   
        if enable_structured_data == '1':
            structured_output, page_number = extract_text_from_textract_withoutsection(json.loads(result_json))
            
            output_string = build_output_string_withoutsection(structured_output)
            #structured_data_folder = os.getenv('ocr_structured_data_folder')
            structured_data_folder = cached_config.get('ocr_structured_data_folder')
            structured_data_suffix = cached_config.get('ocr_structured_data_suffix')
            
            cleanpdf_output_key = f'{structured_data_folder}{filename_without_extension}{structured_data_suffix}.txt'
            # Upload the results to S3
            s3_put_object(output_bucket,cleanpdf_output_key,output_string,'')
        
        #Perform data chunking on the structured data
        #build_segmented_data(output_string,filename_without_extension,output_bucket)
        
        batch_methodname = cached_config.get('batch_methodname')
        batch_jobname = cached_config.get('batch_jobname')
        batch_jobqueue = cached_config.get('batch_jobqueue')
        batch_jobdefinition = cached_config.get('batch_jobdefinition')
        batch_pythoncodefile = cached_config.get('batch_pythoncodefile')
        
        
        #Convert Json results into simple text file (Not the strucutred one)
        if enable_simple_text_file == '1':
            #Transform json into simple text file 
            formatted_text = extract_text_from_textract(json.loads(result_json))
                
            simple_text_input = json.dumps({"text": formatted_text})
            
            #Check if saveCleanpdfs3_featureflag enabled then only save to S3 folder
            if savecleanpdfs3_featureflag:
                cleanpdf_output_key = f'{ocrresults_folder}{clean_outputfilename}.txt'
                print(f'output_bucket: {output_bucket}, key: {cleanpdf_output_key}, formatted text: {simple_text_input}')
                # Upload the results to S3
                s3.put_object(
                    Bucket=output_bucket,
                    Key=cleanpdf_output_key,
                    Body=simple_text_input
                )
            
        #Find case ID and instance id to build file name 
        key_to_find_caseid = "CMS Control Number"
        case_id = find_key_value_in_string(output_string, key_to_find_caseid)
        key_to_find_instanceid = "Instance ID"
        instance_id = find_key_value_in_string(output_string, key_to_find_instanceid)
        
        
        #Once processing is complete, publish to SNS
        custom_payload = {
                    "bucket_name": output_bucket,
                    "job_id": job_id,
                    "input_file_key": s3init_ObjectName,
                    "file_name": filename,
                    "output_file": output_key
                }
        #Construct the message for different protocol
        message_body = {
            "default": json.dumps(custom_payload)
        }        
        print(f"SNS Message for Message: {message_body} ")
        
        response = sns_client.publish(
        TopicArn=topic_arn,
        MessageStructure = 'json',
        Message= json.dumps(message_body),
        Subject="Lambda Process Complete"
        )

        print(f"SNS Message for Job {job_id} with Message: {message_body} ")

        isSuccess = create_update_log_file(output_bucket,s3init_ObjectName,page_number,ocr_configpath)        
                    
        return {
            'statusCode': 200,
            'body': json.dumps('AWS Textract extraction Processing completed successfully')
        }

    except Exception as e:
        print(f"Error processing Textract job batch extraction result: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing Textract job batch extraction result: {e}")
        }


#Get all the results from AWS Textract output from multiple json responses
def get_all_results(job_id):
    all_results = []
    response = textract.get_document_analysis(JobId=job_id)
    all_results.extend(response['Blocks'])

    while 'NextToken' in response:
        next_token = response['NextToken']
        response = textract.get_document_analysis(JobId=job_id, NextToken=next_token)
        all_results.extend(response['Blocks'])
    
    return all_results

#Merge all the json responses from AWS Textract
def merge_results(all_results):
    return json.dumps({'Blocks': all_results})

#Convert json output to simple text file
def extract_text_from_textract(textract_json):
    blocks = textract_json.get('Blocks', [])
    
    # Dictionary to store text per page
    page_text = {}
    
    # Store blocks by their ID for faster lookup (especially for TABLEs)
    block_by_id = {block['Id']: block for block in blocks}

    for block in blocks:
        block_type = block.get('BlockType')
        
        # Initialize page entry if not already present
        page_number = block.get('Page', 1)
        if page_number not in page_text:
            page_text[page_number] = []

        # Handle LINE blocks
        if block_type == 'LINE':
            page_text[page_number].append(block.get('Text', ''))

        # Handle TABLE blocks
        elif block_type == 'TABLE':
            relationships = block.get('Relationships', [])
            if isinstance(relationships, list):
                for relationship in relationships:
                    if relationship.get('Type') == 'CHILD':
                        child_ids = relationship.get('Ids', [])
                        for child_id in child_ids:
                            cell_block = block_by_id.get(child_id)
                            if cell_block and cell_block.get('BlockType') == 'CELL':
                                cell_text = []
                                if 'Relationships' in cell_block:
                                    for rel in cell_block['Relationships']:
                                        if rel.get('Type') == 'CHILD':
                                            for grandchild_id in rel.get('Ids', []):
                                                child_block = block_by_id.get(grandchild_id)
                                                if child_block and child_block.get('BlockType') == 'WORD':
                                                    cell_text.append(child_block.get('Text', ''))
                                page_text[page_number].append(' '.join(cell_text))

        # Handle KEY_VALUE_SET blocks (forms)
        elif block_type == 'KEY_VALUE_SET':
            key_text = value_text = ''
            if 'EntityTypes' in block:
                if 'KEY' in block['EntityTypes']:
                    key_text = block.get('Text', '')
                elif 'VALUE' in block['EntityTypes']:
                    value_text = block.get('Text', '')
            if key_text or value_text:
                page_text[page_number].append(f"'{key_text}: {value_text}'")

    # Combine all text for each page
    combined_text = {page: '\n'.join(texts) for page, texts in page_text.items()}
    
    return combined_text

#Split the large structured file into smaller chunks 
#def build_segmented_data(output_string,file_name_wi,bucket_name,ocr_configpath):
#    
#    if cached_config is None:
#        cached_config = s3_get_object_Json(bucket_name,ocr_configpath)
#    enable_structured_data = cached_config.get('enable_convert_ocr_jsondata_structured')
#    data_segments_folder = cached_config.get('ocr_data_segmentation_folder')
#    datachunking = cached_config.get('enable_data_segmentation')
#    
#    if enable_structured_data == '1' and datachunking == '1':
#        #print(f'Output_string: {output_string}')
#        chunks = chunk_text_by_page(output_string)
#       for i, chunk in enumerate(chunks, 1):
#            file_key = f'{data_segments_folder}{file_name_wi}_chunks/{file_name_wi}_chunk_{i}.txt'
#            #s3.put_object(Bucket=bucket_name, Key=file_key, Body=chunk)
#            s3_put_object(bucket_name,file_key,chunk,'')
    
#Function to insert into s3 bucket
def s3_put_object(bucket_name,file_key,body,metadata):
    if metadata == '':
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=body)
    else:
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=body, Metadata=metadata)

def s3_get_object_Json(bucket_name,file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    log_data = json.loads(response['Body'].read().decode('utf-8'))
    return log_data   

#Extract the textract json data into Structured format Page -> Text, Key-value pairs, Tables
def extract_text_from_textract_withoutsection(textract_json):
    blocks = textract_json.get('Blocks', [])
    
    # Dictionaries to store structured data for each page
    page_content = {}
    
    # Store blocks by their ID for faster lookup
    block_by_id = {block['Id']: block for block in blocks}
    page_number = 0
    for block in blocks:
        block_type = block.get('BlockType')
        page_number = block.get('Page', 1)
        
        # Initialize page entry if not already present
        if page_number not in page_content:
            page_content[page_number] = {
                'KeyValuePairs': [],
                'text': [],
                'tables': []
            }

        # Handle KEY_VALUE_SET blocks (Form extraction)
        if block_type == 'KEY_VALUE_SET':
            key, value = extract_key_value_pair(block, block_by_id)
            if key.strip().endswith(':'):
                key = key.rstrip(':')
                key = key.replace(':','')
            if key != '' or value != '':
                page_content[page_number]['KeyValuePairs'].append({key: value})
          
            
        # Handle LINE blocks (Text extraction)
        elif block_type == 'LINE':
            text_value = block.get('Text', '')
            # Only add if it doesn't already exist in key-value pairs or tables
            if not any(text_value in kv for kv in page_content[page_number]['KeyValuePairs']):
                page_content[page_number]['text'].append(text_value)

        # Handle TABLE blocks (Table extraction)
        elif block_type == 'TABLE':
            table_data = extract_table_data(block, block_by_id)
            ##print(f'table_data {len(table_data)}')
            # Avoid adding table content that is already in text or key-value pairs
            page_content[page_number]['tables'].append(table_data)
                    

   
    return page_content, page_number

#Extract Key-Value pairs from the file
def extract_key_value_pair(block, block_by_id):
    """Extract key-value pair from KEY_VALUE_SET block"""
    key = ""
    value = ""
    
       # Check if the block is a key block
    if 'KEY' in block['EntityTypes']:
        # Extract the key text
        if 'Relationships' in block:
            for rel in block['Relationships']:
                if rel['Type'] == 'CHILD':
                    for child_id in rel['Ids']:
                        key_block = block_by_id[child_id]
                        if key_block['BlockType'] == 'WORD':
                            key += key_block['Text'] + ' '

        # Extract the value text
        if 'Relationships' in block:
            for rel in block['Relationships']:
                if rel['Type'] == 'VALUE':
                    for value_id in rel['Ids']:
                        value_block = block_by_id[value_id]
                        if 'Relationships' in value_block:
                            for val_rel in value_block['Relationships']:
                                if val_rel['Type'] == 'CHILD':
                                    for child_id in val_rel['Ids']:
                                        word_block = block_by_id[child_id]
                                        if word_block['BlockType'] == 'WORD':
                                            value += word_block['Text'] + ' '

    return key, value

#Extract table data from the file
def extract_table_data(table_block, block_by_id):
    """Extract table data by traversing TABLE and CELL blocks"""
    table_data = {"Column Header": [], "Rows": []}
    
    relationships = table_block.get('Relationships', [])
    for relationship in relationships:
        if relationship.get('Type') == 'CHILD':
            child_ids = relationship.get('Ids', [])
            for child_id in child_ids:
                cell_block = block_by_id.get(child_id)
                if cell_block and cell_block.get('BlockType') == 'CELL':
                    cell_text = extract_text_from_cell(cell_block, block_by_id)
                    row_index = cell_block.get('RowIndex', 0)
                    col_index = cell_block.get('ColumnIndex', 0)
                    
                    if row_index == 1:
                        table_data["Column Header"].append(cell_text)
                    else:
                        if len(table_data["Rows"]) < row_index - 1:
                            table_data["Rows"].append([])
                        table_data["Rows"][row_index - 2].append(cell_text)

    return table_data

#Extract cell data for tables from the file
def extract_text_from_cell(cell_block, block_by_id):
    """Extract text from a CELL block in a table"""
    cell_text = []
    if 'Relationships' in cell_block:
        for rel in cell_block['Relationships']:
            if rel.get('Type') == 'CHILD':
                for grandchild_id in rel.get('Ids', []):
                    child_block = block_by_id.get(grandchild_id)
                    if child_block and child_block.get('BlockType') == 'WORD':
                        cell_text.append(child_block.get('Text', ''))
    return ' '.join(cell_text)



#Build output string for without sections where the structure will be Page -> Text, Key-value pair, Tables
def build_output_string_withoutsection(output):
    """Builds a structured text string from the output."""
    output_string = []
    pages = list(output.items())  # Convert to a list to know the length
    total_pages = len(pages)
    output_string.append(f'{{')
    for page, content in output.items():
        output_string.append(f'"Page {page}":"\n')
        
        # Add the text content for the page
        if content.get('text'):
            content_text = [text.replace('\\','/').replace('"', '\\"') for text in content['text']]
            output_string.append(f"  Text: {', '.join(content_text)}\n")
        
        # Add the key-value pairs for the page
        if content.get('KeyValuePairs'):
            output_string.append(f"  Key-Value Pairs:\n")
            for kvp in content['KeyValuePairs']:
                for key, value in kvp.items():
                    content_key = key.replace('\\','/').replace('"','\\"')
                    content_value = value.replace('\\','/').replace('"','\\"')
                    output_string.append(f"    {content_key}: {content_value}\n")
        
        # Add the tables for the page
        if content.get('tables'):
            output_string.append(f"  Tables:\n")
            for table_index, table_data in enumerate(content['tables'], start=1):
                output_string.append(f"    Table {table_index}:\n")
                column_header = ', '.join(table_data['Column Header']).replace('\\','/').replace('"', '\\"')
                output_string.append(f"      Column Header: {column_header}\n")
                for row_index, row in enumerate(table_data['Rows'], start=1):
                    row_v = ', '.join(row).replace('\\','/').replace('"', '\\"')
                    output_string.append(f"      Row{row_index}: {row_v}\n")
        
        
        if page == total_pages:
            output_string.append(f'"\n')
        else:
            output_string.append(f'",\n')
            
    output_string.append(f'}}')
    return ''.join(output_string)

#Chunk data from the larger files in smaller one based on 10000 char limit.
def chunk_text_by_page(text, page_marker='"Page', char_limit=10000):
    chunks = []
    lines = text.splitlines()
    chunk = []
    
    for line in lines:
        if line.startswith(page_marker) and chunk:
            current_chunk = "\n".join(chunk)
            chunks.append(current_chunk)
            chunk = [line]
        else:
            chunk.append(line)
    if chunk:
        chunks.append("\n".join(chunk))
    
    # Separate chunks based on char_limit
    final_chunks = []
    temp_chunk = ""
    
    for chunk in chunks:
        if len(temp_chunk) + len(chunk) > char_limit:
            temp_chunk = temp_chunk.lstrip("{")
            temp_chunk = temp_chunk.rstrip(",}")
            temp_chunk = temp_chunk.replace('{"','"')
            final_chunks.append(f"{{{temp_chunk}}}")
            temp_chunk = chunk
            
        else:
           temp_chunk += "\n" + chunk
                
    if temp_chunk:
        temp_chunk = temp_chunk.rstrip(",")
        temp_chunk = temp_chunk.lstrip("{{")
        temp_chunk = temp_chunk.rstrip("}}")
        final_chunks.append(f"{{{temp_chunk}}}")
    
    return final_chunks
    
#This function use to find a Key-value is already present in the text to avoid duplication
def find_key_value_in_string(text, key):
    """Search for a key in the string and return the associated value."""
    # Compile a regex pattern to match the key followed by a colon and the associated value
    pattern = re.compile(rf"{key}\s*:\s*(\S+)")
    
    # Search the string for the key and associated value
    match = pattern.search(text)
    
    if match:
        return match.group(1)  # Return the first matching group (the value)
    
    return None  # If the key is not found

# Function to count instances of a text string across all pages
def count_text_across_pages(structured_output, target_text):
    total_count = 0
    
    for page_num, page_data in structured_output.items():
        if "text" in page_data:  # Ensure the page has a 'text' field
            total_count += page_data["text"].count(target_text)  # Count in each page's text
    
    return total_count
    

def is_section_header(text, left_position, threshold=0.03):
    """Heuristic to detect section headers based on text and position"""
    return left_position < threshold 

def create_update_log_file(bucket_name,object_key, page_number,ocr_configpath):
    #S3 bucket and file details
    #env_processlog = os.getenv('processlog')
    
    cached_config = s3_get_object_Json(bucket_name,ocr_configpath)

    env_processlog = cached_config.get('ocr_processlog')
    logfile_name_dateformat = cached_config.get('logfile_name_dateformat')
    
    foldername, filename = object_key.split('/')
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    
    new_object_key = f"{env_processlog}{datetime.now().strftime('%m%Y')}.json"
    logfile_status = cached_config.get('logfile_status_end')
    logfile_status_message = cached_config.get('logfile_status_message_end')
    
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    file_size = response['ContentLength']
    print(f'bucket name : {bucket_name}, object key: {object_key}, file size: {file_size}')
   
    # File content
    body = {
        "bucketname": bucket_name,
        "filepath": object_key,
        "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "filesize": file_size,
        "pagecount": page_number,
        "status": logfile_status,
        "message": logfile_status_message
    }
    
    #print(f'bucket name : {bucket_name}, object key: {new_object_key}, body: {body}')
    #Check if object exists already then update it or create new object 
    object_exists = check_if_object_exists(bucket_name,new_object_key)
    if object_exists:
        #get existing Log
        log_data = s3_get_object_Json(bucket_name,new_object_key)
        log_data.append(body)
    else:
        log_data = [body]
       
    s3_put_object(bucket_name,new_object_key,json.dumps(log_data),'')
    return "success"

def check_if_object_exists(bucket, key):
    try:
        # Try to get metadata about the object
        s3.head_object(Bucket=bucket, Key=key)
        return True  # If no exception, the object exists
    except ClientError as e:
        # If an error occurs, the object does not exist or there is a permission issue
        if e.response['Error']['Code'] == '404':
            return False  # Object not found
        else:
            # Reraise the error if it's another type
            raise
    
def load_env_from_dockerfile(file_path):
    with open(file_path) as f:
        for line in f:
            # Ignore comments and empty lines
            if line.startswith('#') or not line.strip():
                continue

            # Check if line starts with 'ENV'
            if line.startswith('ENV'):
                # Split 'ENV' and the actual key=value pair
                _, key_value = line.split(' ', 1)

                # Remove any quotes and split into key and value
                key, value = key_value.strip().replace('"', '').split('=', 1)

                # Set the environment variable in os.environ
                os.environ[key] = value

def main():
    # Ensure that enough arguments are passed to the script
    if len(sys.argv) < 5:
        print("Not enough arguments provided!")
        sys.exit(1)

     # Extract the arguments
    method_name = sys.argv[1]  # The function name passed as a string (process_textract_job)
    job_id = sys.argv[2]
    bucket_name = sys.argv[3]
    input_file = sys.argv[4]
    config_path = sys.argv[5]    

    if method_name == "process_textract_job":
        process_textract_job(job_id, bucket_name, input_file, config_path)
    else:
        print(f'Passed method {method_name} is not recorgnized!')
        sys.exit(1)

if __name__ == "__main__":
    # This ensures the script runs the main function when executed directly
    main()