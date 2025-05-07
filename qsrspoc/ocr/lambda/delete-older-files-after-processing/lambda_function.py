import boto3
import os
import json
from datetime import datetime, timedelta, timezone

s3 = boto3.client('s3')

cached_config = None


def s3_get_object_Json(bucket_name,file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    log_data = json.loads(response['Body'].read().decode('utf-8'))
    return log_data  

def lambda_handler(event, context):
    
    bucket_name = os.environ.get("bucket_name")
    global cached_config
    ocr_configpath = os.getenv('ocr_configpath')
    #Get config json
    cached_config = s3_get_object_Json(bucket_name,ocr_configpath)
    
    #Get the configurable values from config files in s3 /config/ocr/ 
    folder_paths_str = cached_config.get("deletion_files_folder_paths")
    age_threshold_str = cached_config.get("deletion_files_age_threshold_in_days")

    if not bucket_name or not folder_paths_str:
        raise ValueError("BUCKET_NAME and FOLDER_PATHS environment variables are required.")

    age_threshold_tmp = int(age_threshold_str)
    age_threshold = timedelta(days=age_threshold_tmp)
    #based on the age threshold the number of days caludated for deletion (Means how many days old files needs to be delete)
    cutoff_time = datetime.now(timezone.utc) - age_threshold
    folder_paths = [p.strip() for p in folder_paths_str.split(",") if p.strip()]
    total_deleted = 0
    folder_deletion_summary = {}
    
    #Loop through each folder speciifed in config files such as "ocr-results/" or "structured-data/"
    for prefix in folder_paths:
        print(f"Scanning prefix '{prefix}' in bucket '{bucket_name}'")

        deleted_in_folder = 0
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        #Loop through each files in the specified prefix value 
        for page in pages:
            for obj in page.get('Contents', []):
                key = obj['Key']
                last_modified = obj['LastModified']
                
                # Skip "folder" keys like "folder1/" that have no content
                if key.endswith('/') and obj.get('Size', 0) == 0:
                    continue

                if last_modified < cutoff_time:
                    print(f"Deleting: {key} (LastModified: {last_modified})")
                    s3.delete_object(Bucket=bucket_name, Key=key)
                    deleted_in_folder  += 1
                    
        folder_deletion_summary[prefix] = deleted_in_folder    
        total_deleted += deleted_in_folder
        print(f"✅ Deleted {deleted_in_folder} file(s) from '{prefix}'")
    
    # Log final summary
    print("\n📋 Deletion Summary:")
    for folder, count in folder_deletion_summary.items():
        print(f" - {folder}: {count} files deleted")

    print(f"\n🧹 Total files deleted: {total_deleted}")

    return {
        'statusCode': 200,
        'body': {
            'folder_deletion_summary': folder_deletion_summary,
            'total_deleted': total_deleted
        }
    }


