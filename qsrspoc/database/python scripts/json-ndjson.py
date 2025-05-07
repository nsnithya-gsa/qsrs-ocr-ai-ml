import json
import boto3
import os
import re  # Using regex for better pattern extraction
from datetime import datetime

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        source_bucket = event['Records'][0]['s3']['bucket']['name']  # Bucket Name
        source_key = event['Records'][0]['s3']['object']['key']  # File Path
        destination_bucket = "log-files-for-athena"
        destination_key = f"converted_{source_key}"

        # Fetch the source file
        response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
        source_content = response['Body'].read().decode('utf-8')
        new_records = json.loads(source_content)
        print(f"New records: {new_records}")

        # Retrieve metadata for last processed count
        try:
            existing_response = s3_client.head_object(Bucket=destination_bucket, Key=destination_key)
            last_record_count = int(existing_response['Metadata'].get('last_record_count', 0))
        except s3_client.exceptions.ClientError:
            last_record_count = 0  # First time processing

        print(f"Last record count: {last_record_count}")

        # Get only newly appended records
        new_data_records = new_records[last_record_count:]
        print(f"New data records: {new_data_records}")

        # Fetch existing file content if it exists
        try:
            existing_response = s3_client.get_object(Bucket=destination_bucket, Key=destination_key)
            existing_content = existing_response['Body'].read().decode('utf-8')
            existing_records = existing_content.splitlines()
        except s3_client.exceptions.NoSuchKey:
            existing_records = []

        print(f"Existing records: {existing_records}")

        # Function to extract only the original PDF filename
        def extract_original_filename(filepath):
            match = re.match(r'^(?:.*/)?([^_/]+_Redacted)', filepath)  # Extract clean filename
            return match.group(1) + ".pdf" if match else ""


        # Transform records and correctly extract "File"
        transformed_records = []
        for record in new_data_records:
            original_filename = extract_original_filename(record.get("filepath", ""))

            transformed_record = {
                "Bucket Name": record.get("bucketname", ""),
                "File Path": record.get("filepath", ""),
                "File": original_filename,  # Extracts clean file name
                "Execution Datetime": record.get("datetime", ""),
                "File Size": record.get("filesize", ""),
                "Page Count": None if record.get("pagecount") == "NA" else record.get("pagecount"),  # Convert "NA" to None
                "Status": record.get("status", ""),
                "Message": record.get("message", "")
            }
            # Add "Num Question" only if it exists in the original record
            if "num_questions" in record:
                transformed_record["Num Question"] = record["num_questions"]

            transformed_records.append(json.dumps(transformed_record))

        combined_records = existing_records + transformed_records
        combined_content = "\n".join(combined_records)

        print(f"Combined content: {combined_content}")

        # Upload with updated metadata (tracking processed record count)
        s3_client.put_object(
            Bucket=destination_bucket,
            Key=destination_key,
            Body=combined_content,
            Metadata={'last_record_count': str(len(new_records))}
        )

        print(f"File successfully processed and appended to {destination_bucket}/{destination_key} at {datetime.now()}")

    except Exception as e:
        print(f"Error: {e}")
        raise e