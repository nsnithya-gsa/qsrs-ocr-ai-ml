import json
import boto3
import os

s3_client = boto3.client('s3')
cached_config = None

def lambda_handler(event, context):
    
    global cached_config
    # Loop through each record (message) in the SQS event
    for record in event['Records']:
        # Parse the message body and extract the job ID
        message_body = json.loads(record['body'])
        print(f"Message Body: {message_body}")
        #Get config json
        ocr_configpath = os.getenv('ocr_configpath')
        
        custom_message = json.loads(message_body["Message"])
        # Define bucket and folders
        bucket_name = custom_message["bucket_name"]
        source_file_key = custom_message["input_file_key"]
        source_file_name = custom_message["file_name"] 
        output_file_key = custom_message["output_file"]
        
        cached_config = s3_get_object_Json(bucket_name,ocr_configpath)
        destination_folder = cached_config.get('archive_destinationfolder')
        newfile_name_suffix = cached_config.get('archive_newfilenamesuffix')
        
        filename_without_extension = os.path.splitext(os.path.basename(source_file_name))[0]
        destination_file_key = f"{destination_folder}{filename_without_extension}{newfile_name_suffix}.pdf"
        
        ocr_pdf_preprocess = cached_config.get('ocr_pdf_preprocess_folder')
        ocr_pdf_preprocess_folder_prefix = f"{ocr_pdf_preprocess}{filename_without_extension}/"
            
        ocr_pdf_split_results = cached_config.get('ocr_pdf_split_results_folder')
        ocr_pdf_split_results_folder_prefix = f"{ocr_pdf_split_results}{filename_without_extension}/"
            
        try:
            #Copy the file to the destination folder
            s3_client.head_object(Bucket=bucket_name,Key=source_file_key)
            # If the file exists, copy it to the destination folder
            s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': source_file_key},
                Key=destination_file_key
            )
            #Now that the Copy is Successful, delete the file from source folder 
            s3_client.delete_object(Bucket=bucket_name, Key=source_file_key)
            
            
            #Delete the folder from ocr-pdf-preprocess/
            s3_delete_folder(bucket_name=bucket_name, folder_prefix=ocr_pdf_preprocess_folder_prefix)
            #Delete the folder from ocr-pdf-split-results/
            s3_delete_folder(bucket_name=bucket_name, folder_prefix=ocr_pdf_split_results_folder_prefix)
            return{
                'statusCode': 200,
                'body': json.dumps(f"File '{source_file_name}' moved successfully from {source_file_key} to {destination_file_key}")
            }

        except Exception as e:
            print(f"Error moving file result: {e}")
            return{
                 'statusCode': 500,
                 'body': json.dumps(f"Error moving file: {str(e)}")
            }

#Get files from S3 bucket in json format   
def s3_get_object_Json(bucket_name,file_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    log_data = json.loads(response['Body'].read().decode('utf-8'))
    return log_data        

#Delete folders from S3 bucket
def s3_delete_folder(bucket_name, folder_prefix):

    objects_to_delete = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
    
    if 'Contents' in objects_to_delete:
        delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete['Contents']]
        s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_keys})
        print(f"Deleted all objects under {folder_prefix}")
    else:
        print("Folder empty or doesn't exist.")
