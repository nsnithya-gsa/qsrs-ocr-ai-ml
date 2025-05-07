import json
import urllib.parse
import time
import os
import re
import boto3
import botocore
from datetime import datetime
from botocore.exceptions import ClientError
# Initialize boto3 clients for Textract,SNS, batch and S3
textract = boto3.client('textract')
s3 = boto3.client('s3')
sns_client = boto3.client('sns')
batch_client = boto3.client('batch')

cached_config = None

def lambda_handler(event, context):
    try:
        global cached_config
        # Loop through each record (message) in the SQS event
        for record in event['Records']:
            # Parse the message body and extract the job ID
            message_body = json.loads(record['body'])
            
            #Load textract message and load as json to extract JobId and Status
            textract_message = json.loads(message_body['Message'])
            job_id = textract_message['JobId']
            status = textract_message['Status']
            print(f"job_id: {job_id}, status: {status} ")
            #Initialize the variables and assign the values
            s3init_ObjectName = textract_message['DocumentLocation']['S3ObjectName']
            output_bucket = textract_message['DocumentLocation']['S3Bucket']
            
            # Split at the last '/' to separate the folder path and filename
            foldername, filename = s3init_ObjectName.split('/', 1)
            filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
            foldername, filename = filename.split('/') 
            
            #Get Global variables and Environment variable values 
            ocr_configpath = os.getenv('ocr_configpath')
            cached_config = s3_get_object_Json(output_bucket,ocr_configpath)
            ocrresults_file_suffix = cached_config.get('ocr_results_suffix')
            outputfilename = (f"{filename_without_extension}{ocrresults_file_suffix}")
            ocr_pdf_split_results_folder = cached_config.get('ocr_pdf_split_results_folder')
            ocrresults_folder = cached_config.get('ocr_resultsfolder')
            savecleanpdfs3_featureflag = cached_config.get('savecleanpdfs3')
            output_key = f'{ocr_pdf_split_results_folder}{foldername}/{outputfilename}.json'
            
            # Check if the job completed successfully and store Json file in S3
            if status == "SUCCEEDED":
                
                # Call Textract to get the job results
                all_results = get_all_results(job_id)
                #Merge all the results in one Json file
                result_json = merge_results(all_results)
                
                #Add Job_id into metadata of the json file that will be stored in S3
                metadata = {'AWS Textract jobid': f'{job_id}'}
               
                # Upload the AWS Textract json output results to S3 
                s3_put_object(output_bucket,output_key,result_json,metadata)
                print(f"output_bucket: {output_bucket}, output_key: {output_key},, metadata: {metadata}")
                
            else:
                print(f"Textract job {job_id} did not succeed. Status: {status}")
                
        return {
            'statusCode': 200,
            'body': json.dumps('Processing completed successfully')
        }

    except Exception as e:
        print(f"Error processing Textract job result: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing Textract job result: {e}")
        }


#Get all the results from AWS Textract output from multiple json responses
def get_all_results(job_id):
    all_results = []
    max_retries = 1
    retries = 0
    while retries < max_retries:
        try:
            response = textract.get_document_text_detection(JobId=job_id)
            # Exit loop if successful
            break
        except botocore.exceptions.ClientError as error: 
            error_code = error.response['Error']['Code']
            #Retries in case of Throttling errors
            if error_code == 'ProvisionedThroughputExceededException':
                wait_time = (2 ** retries) + random.uniform(0, 1)
                print(f"Throttled. Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                # If it's a different error, re-raise it
                raise
    
    all_results.extend(response['Blocks'])

    while 'NextToken' in response:
        next_token = response['NextToken']
        response = textract.get_document_text_detection(JobId=job_id, NextToken=next_token)
        all_results.extend(response['Blocks'])
    
    return all_results

#Merge all the json responses from AWS Textract
def merge_results(all_results):
    return json.dumps({'Blocks': all_results})

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

#Create and update data in a log file 
def create_update_log_file(bucket_name,object_key, page_number):
    #S3 bucket and file details
    #env_processlog = os.getenv('processlog')
    env_processlog = cached_config.get('ocr_processlog')
    logfile_name_dateformat = cached_config.get('logfile_name_dateformat')
    
    foldername, filename = object_key.split('/', 1)
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    """Split at the last '/' to separate the folder path and filename"""
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
        "pagecount": f"{page_number}",
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

#Check to see if object already exists in S3 
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