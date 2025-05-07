import json
import boto3

s3 = boto3.client('s3')

# Get utils
def get_bucket() -> str:
    for possible_bucket in [
        'qsrs-ocr-poc-dev',
        'ahrq-qsrs-ml-poc'
    ]:
        x = boto3.resource('s3').Bucket(possible_bucket)
        if x.creation_date is not None:
            return possible_bucket
    return None
import sys
sys.path.append('/tmp')
s3.download_file(get_bucket(), 'ai-ml/code/utils.py', '/tmp/utils.py')
import utils

def lambda_handler(event, context):
    # EVENT: page-embeddings folder is added to - 1
    # (actually triggered via Step function, but passing along the pathing information)

    print(event)

    # Step 1: Extract S3 bucket and file information from the event
    bucket, key, input_folder, input_file = utils.get_s3_paths(event)
    algorithm = event['algorithm']
    # Input file ex: Test123_datetime_HASH_embeddings.json
    
    # Log process start 
    #utils.create_update_log_file(key=key, message=f"Algorithm {algorithm} started", job_start=True)
    
    # Step 2: Download vector embeddings & page text from S3
    embeddings_key = key
    all_page_text_file = utils.get_matching_pdf_text_FILE(page_embeddings_file=input_file)

    # Step 3: Select questions for this specific algorithm
    prompts = utils.load_questions(algorithm=algorithm)

    # Step 4: Read the JSON file that stores passed data and algorithm event recordings
    passed_data = utils.retrieve_data_passing_file(page_embeddings_key = embeddings_key)

    return {
        'algorithm': algorithm,
        'embeddings_key': embeddings_key,
        'all_page_text_file': all_page_text_file,
        'prompts': prompts,
        'passed_data': passed_data,
    }