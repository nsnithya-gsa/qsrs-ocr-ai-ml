import json
import urllib.parse
import time
import os
import re
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
# Initialize boto3 clients for Textract and S3
textract = boto3.client('textract')
s3 = boto3.client('s3')
sns_client = boto3.client('sns')
batch_client = boto3.client('batch')

cached_config = None

def lambda_handler(event, context):
    try:
        record = event["Records"][0]
        bucket_name = record['s3']['bucket']['name']
        input_s3_key = record["s3"]["object"]["key"]  # Example: "ocr-results/4928968_Redacted_ocrresults.json"
        ocrresults_filename_only = os.path.basename(input_s3_key) # Example: "4928968_Redacted_ocrresults.json"
        filename_without_extension = os.path.splitext(os.path.basename(ocrresults_filename_only))[0] # Example: "4928968_Redacted_ocrresults"
         
        ocr_configpath = os.getenv('ocr_configpath')
        topic_arn = os.getenv('topicarn') 
        cached_config = s3_get_object_Json(bucket_name,ocr_configpath)
        ocr_resultsfolder = cached_config.get('ocr_resultsfolder')
        ocr_results_suffix = cached_config.get('ocr_results_suffix')
        ocr_processing_landing = cached_config.get('ocr-processing-landing')
        output_bucket = bucket_name
        outputfilename = filename_without_extension
        output_key = f'{ocr_resultsfolder}{outputfilename}.json'
        pdf_filename = ocrresults_filename_only.replace("_ocrresults.json", ".pdf")
        pdf_key = f"{ocr_processing_landing}{pdf_filename}"
        
        #Get Textract document analysis results
        # Parse the message body and extract the job ID
       
        foldername, filename = input_s3_key.split('/', 1)
        
        input_s3_key = urllib.parse.unquote_plus(input_s3_key)
        filename = urllib.parse.unquote_plus(filename)
        foldername = urllib.parse.unquote_plus(foldername)
        filename_without_extension = urllib.parse.unquote_plus(filename_without_extension)
        pdf_key = urllib.parse.unquote_plus(pdf_key)
        pdf_filename = urllib.parse.unquote_plus(pdf_filename)
        output_key = urllib.parse.unquote_plus(output_key)
        
        result_json = s3_get_object_Json(output_bucket, input_s3_key)
        
        #Get Global variables and Environment variable values 
        cached_config = s3_get_object_Json(output_bucket,ocr_configpath)
       
        #json data to convert into structured text file   
        structured_output, page_number = extract_text_from_textract_withoutsection(result_json)
        
        output_string = build_output_string_withoutsection(structured_output)
        #structured_data_folder = os.getenv('ocr_structured_data_folder')
        structured_data_folder = cached_config.get('ocr_structured_data_folder')
        structured_data_suffix = cached_config.get('ocr_structured_data_suffix')
        filename_without_extension = filename_without_extension.replace("_ocrresults", "")
        cleanpdf_output_key = f'{structured_data_folder}{filename_without_extension}{structured_data_suffix}.txt'
        # Upload the results to S3
        s3_put_object(output_bucket,cleanpdf_output_key,output_string,'')
        
        #Once processing is complete, publish to SNS
        custom_payload = {
                    "bucket_name": output_bucket,
                    "input_file_key": pdf_key,
                    "file_name": pdf_filename,
                    "output_file": output_key
                }
        #Construct the message for different protocol
        message_body = {
            "default": json.dumps(custom_payload)
        }        
        print(f"SNS Message for Message: {message_body} ")
        
        isSuccess = create_update_log_file(output_bucket,pdf_key,page_number,ocr_configpath)
        
        response = sns_client.publish(
        TopicArn=topic_arn,
        MessageStructure = 'json',
        Message= json.dumps(message_body),
        Subject="Structured file generation Process Complete"
        )

        print(f"SNS Message for file {pdf_key} with Message: {message_body} sent")
        
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
        else:
            content_text = f"This page {page} is blank"  
            output_string.append(f"  Text: {content_text}\n")
        
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

#Create and Update data in a log file in S3 
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
    
