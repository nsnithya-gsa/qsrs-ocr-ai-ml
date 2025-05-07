import json
import urllib.parse
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
s3 = boto3.client('s3')

# Configuration Variables
SOURCE_BUCKET = os.environ.get('SOURCE_BUCKET', os.getenv('source_bucket'))
DESTINATION_BUCKET = os.environ.get('DESTINATION_BUCKET', os.getenv('destination_bucket'))

cached_config = None

#Count existing files in bucket
def count_existing_files(bucket, prefix):
    """Count files in the destination folder"""
    response1 = s3.list_objects_v2(Bucket=DESTINATION_BUCKET, Prefix=prefix)
    file_count = sum(1 for obj in response1.get('Contents', []) if obj['Key'] != prefix)
    return file_count  # Return count of files (or 0 if empty)

def lambda_handler(event, context):
    try:
        global cached_config
        ocr_configpath = os.getenv('ocr_configpath')
        #Get config json
        cached_config = s3_get_object_Json(DESTINATION_BUCKET,ocr_configpath)
        
        #Retrieve variable information from a config.json file
        number_of_documents = int(cached_config.get('ocr-dms-dl-number-of-documents')) #number fof documents to copy from drop location at one time
        source_folder = cached_config.get('ocr-cms-dl-landing') 
        destination_folder = cached_config.get('ocr-processing-landing')
        archive_folder = cached_config.get('ocr-cms-dl-archive')
        enable_existing_filecheck = cached_config.get('ocr-dms-dl-enable-existing-filecheck') #Flag to check number of files in progress destination folder
        
        # List objects from the source bucket
        response = s3.list_objects_v2(Bucket=SOURCE_BUCKET, Prefix=source_folder)
        
        #Remove the folder row from the content and only get the list of files
        response['Contents'] = [obj for obj in response['Contents'] if not obj['Key'].endswith('/')]
        
        if 'Contents' not in response:
            print("No files found in the source bucket.")
            return {"message": "No files to process"}

        # Sort files by LastModified date (ascending: oldest first)
        sorted_files = sorted(response['Contents'], key=lambda x: x['LastModified'])
        
        print(f"enable_existing_filecheck: {enable_existing_filecheck}")
        
        if enable_existing_filecheck == "1":
            # Step 1: Count existing files in the destination folder
            existing_files_count = count_existing_files(DESTINATION_BUCKET, destination_folder)
            number_of_documents = number_of_documents - existing_files_count
            print(f'existing_files_count: {existing_files_count},number_of_documents: {number_of_documents} ')
        
        # Select up to MAX_FILES from the sorted list
        files_to_copy = sorted_files[:number_of_documents]
        
            
        files_copied = 0
        for obj in files_to_copy:
            file_key = obj['Key']
            file_name = file_key.split("/")[-1]  # Extract only file name
            copy_source = {'Bucket': SOURCE_BUCKET, 'Key': file_key}
            
            # Define the new destination path inside the folder
            destination_key = f"{destination_folder}{file_name}"  
            archive_key = f"{archive_folder}{file_name}"  
            print(f'Copy Source: {copy_source}, Source Bucket: {SOURCE_BUCKET}, File Key: {file_key}, Destination Bucket: {DESTINATION_BUCKET}, Destination Key:{destination_key}')
            
            #Step 1
            # Copy file to the destination bucket
            s3.copy_object(CopySource=copy_source, Bucket=DESTINATION_BUCKET, Key=destination_key)
            
            #Step 2
            ##After copying archive the file to archive folder and delete from cms-drop-location
            s3.copy_object(
                Bucket=SOURCE_BUCKET,
                CopySource={'Bucket': SOURCE_BUCKET, 'Key': file_key},
                Key=archive_key
            )
            
            #Step 3
            #Now that Copy function is Successful, delete the file from source folder 
            s3.delete_object(Bucket=SOURCE_BUCKET, Key=file_key)
            
            files_copied += 1
        
        print (f'Successfully copied {files_copied} files from the path {SOURCE_BUCKET}/{source_folder} to the path {DESTINATION_BUCKET}/{destination_folder}.')
        return {"message": f"Successfully copied {files_copied} files from the path {SOURCE_BUCKET}/{source_folder} to the path {DESTINATION_BUCKET}/{destination_folder}."}
    
    except Exception as e:
        print(f"Error while copying files : {str(e)}")
        return {"error": str(e)}
        
        
#get s3 files from bucket in json format
def s3_get_object_Json(bucket_name,file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    log_data = json.loads(response['Body'].read().decode('utf-8'))
    return log_data  