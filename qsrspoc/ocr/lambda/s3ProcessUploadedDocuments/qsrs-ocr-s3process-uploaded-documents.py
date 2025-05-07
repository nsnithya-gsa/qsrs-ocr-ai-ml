import json
import urllib.parse
import os
import boto3
import fitz  # PyMuPDF
from datetime import datetime
from botocore.exceptions import ClientError
s3 = boto3.client('s3')

cached_config = None

def lambda_handler(event, context):
    # Initialize S3 and Textract clients
    global cached_config
    textract = boto3.client('textract')
    
    
    # Extract bucket name and object key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    object_key_without_extension = os.path.splitext(object_key)[0]
    ocr_configpath = os.getenv('ocr_configpath')
    
    #Get config json
    cached_config = s3_get_object_Json(bucket_name,ocr_configpath)

    #Output bucket and prefix name
    output_bucket = bucket_name
    output_prefix = cached_config.get('ocr_resultsfolder')
    
    #env_ocrfeaturetypes = os.getenv('ocr_featuretypes')
    env_ocrfeaturetypes = cached_config.get('ocr_featuretypes')
    pdf_split_size = int(cached_config.get('ocr_pdf_split_size'))
    ocr_pdf_preprocess_s3folder = cached_config.get('ocr_pdf_preprocess_folder')
    
    # Download the file
    file_path = f"/tmp/{object_key.split('/')[-1]}"
    s3.download_file(bucket_name, object_key, file_path)

    try:
        isSuccess = create_update_log_file(bucket_name,object_key)
        split_and_upload_pdf(file_path, bucket_name, object_key_without_extension, pdf_split_size, ocr_pdf_preprocess_s3folder)
       
        return {
            'statusCode': 200,
            'body': json.dumps('Textract job started successfully')
        }

    except Exception as e:
        # Log the exception and return a 500 error code
        print(f"Error processing file from bucket {bucket_name} with key {object_key}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error starting Textract job')
        }


def create_update_log_file(bucket_name,object_key):
    # S3 bucket and file details
    env_processlog = cached_config.get('ocr_processlog')
    logfile_name_dateformat = cached_config.get('logfile_name_dateformat')
    foldername, filename = object_key.split('/')
    filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
    
    new_object_key = f"{env_processlog}{datetime.now().strftime('%m%Y')}.json"
    logfile_status = cached_config.get('logfile_status_start')
    logfile_status_message = cached_config.get('logfile_status_message_start')
    
    response = s3.head_object(Bucket=bucket_name, Key=object_key)
    file_size = response['ContentLength']
    
    print(f'bucket name : {bucket_name}, object key: {object_key}, file size: {file_size}')
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # File content
    body = {
        "bucketname": bucket_name,
        "filepath": object_key,
        "datetime": date_time,
        "filesize": file_size,
        "pagecount": "NA",
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

# This method uses to split pdf, upload to s3 and call process_pdf function to initiate OCR process by calling AWS Textract
def split_and_upload_pdf(file_path, bucket_name, original_key, pdf_split_size, ocr_pdf_preprocess_s3folder):
    pdf_document = fitz.open(file_path)
    num_pages = pdf_document.page_count
    print(f"file_path: {file_path}, bucket name: {bucket_name}, original_key: {original_key}, pdf_split_size: {pdf_split_size}, ocr_pdf_preprocess: {ocr_pdf_preprocess_s3folder}")
    
    # Split in chunks of configurable number of pages from config.json
    chunk_size = pdf_split_size  # Adjust based on testing
    total_splits = (num_pages + chunk_size - 1) // chunk_size  # Total chunks
    for i in range(0, num_pages, chunk_size):
        new_pdf = fitz.open()
        for j in range(i, min(i + chunk_size, num_pages)):
            new_pdf.insert_pdf(pdf_document, from_page=j, to_page=j)

        chunk_filename = f"/tmp/{os.path.basename(original_key)}_part_{i//chunk_size+1}.pdf"
        new_pdf.save(chunk_filename)

        s3_key = f"{ocr_pdf_preprocess_s3folder}{os.path.basename(original_key)}/{os.path.basename(original_key)}_part_{i//chunk_size+1}.pdf"
        s3.upload_file(chunk_filename, bucket_name, s3_key, ExtraArgs={"Metadata": {"total_p": str(total_splits)}})
        
        # Trigger Textract for each split file 
        process_pdf(bucket_name, s3_key)
        print(f"Textract Job started successfully for {s3_key}")

#Initiate async OCR process for a pdf after split and send notification once completed 
def process_pdf(bucket_name, object_key):
    textract = boto3.client('textract')
    env_snstopicarn = os.getenv('snstopicarn')
    env_rolearn = os.getenv('rolearn')
    featuretypes = json.loads(cached_config.get('ocr_featuretypes'))  # Convert string to list
    # Trigger asynchronous Textract job for document text detection 
    text_detection_response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key
            }
        },
        
        NotificationChannel={
            'SNSTopicArn': env_snstopicarn,
            'RoleArn': env_rolearn
        },
    )
    print(f"{text_detection_response}")
    return text_detection_response

#This method to get S3 files in json format
def s3_get_object_Json(bucket_name,file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    log_data = json.loads(response['Body'].read().decode('utf-8'))
    return log_data        
#to add file in S3 folder      
def s3_put_object(bucket_name,file_key,body,metadata):
    if metadata == '':
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=body, ContentType='application/json')
    else:
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=body, Metadata=metadata, ContentType='application/json')

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