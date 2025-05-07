import json
import boto3
from typing import List
import time

s3 = boto3.client('s3')

def get_my_config():
    response = s3.get_object(Bucket='qsrs-ocr-poc-dev', Key='config/ai-ml/config.json')
    data = response['Body'].read().decode('utf-8')
    config = json.loads(data, strict=False)
    return config

import sys
sys.path.append('/tmp')
#Download utils file
s3.download_file('qsrs-ocr-poc-dev', 'ai-ml/code/utils.py', '/tmp/utils.py')
import utils

# Get config file
CONFIG = get_my_config()
#Get output file based on the input file
def output_file_from_input(input_bucket: str, input_folder: str, input_file: str) -> List[str]:
    # Output bucket + folder are easy
    output_bucket = input_bucket
    output_folder = CONFIG['embeddings-folder']
    
    ### Get output filename
    output_file = input_file.replace(CONFIG['cleaned-extension'], CONFIG['embeddings-extension'])

    output_key = output_folder + output_file

    return output_bucket, output_key, output_folder, output_file

#Process file embeddings
def process_file_embeddings(bucket, key, input_folder, input_file):
    t1 = time.time()
    # EVENT: textract text output is cleaned, "cleaned" folder is added to
    
    # Step 1: Log process start
    utils.create_update_log_file(key=key, message="Page embeddings started", job_start=True)

    # Step 2: Download the text file from S3
    text_data = utils.load_s3_json(key=key, bucket=bucket, json_key=None)
    
    # Step 3: Call SageMaker Endpoint to get embeddings, once per page
    embeddings_1d = {} # dict like {str: (768,) }
    for pagenum, page in text_data.items(): 
        if page.strip():  # Check if the page is not empty or just whitespace
            print(utils.get_current_pagenum(pagenum), '/', utils.get_max_pagenum(text_data))
            embeddings_1d[pagenum] = utils.query_embeddings_endpoint(page)
        else:
            # Handle the case when the page is empty, e.g., logging or setting a default value
            print(utils.get_current_pagenum(pagenum), '/', utils.get_max_pagenum(text_data), " / Has blank text")
            embeddings_1d[pagenum] = {}  
    
    # Step 4: Prepare the output key and write embeddings to a new file in S3
    output_bucket, output_key, output_folder, output_file = output_file_from_input(bucket, input_folder, input_file)
    embeddings_data = json.dumps(embeddings_1d)
    
    s3.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=embeddings_data
    )
    
    # Step 4.5: Log process end
    utils.create_update_log_file(key=key, message="Page embeddings finished", job_start=False)

    t2 = time.time()
    print(f'This took {t2-t1:.2f} seconds')
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Embeddings generated and saved to S3.',
            'output_file': output_key
        })
    }


def main():
    # Ensure that enough arguments are passed to the script
    if len(sys.argv) < 5:
        print("Not enough arguments provided!")
        sys.exit(1)

     # Extract the arguments
    method_name = sys.argv[1]  # The function name passed as a string (process_file_embeddings_job)
    bucket_name = sys.argv[2]
    object_key = sys.argv[3]
    input_folder = sys.argv[4]
    input_file = sys.argv[5]    

    if method_name == "process_file_embeddings_job":
        process_file_embeddings(bucket_name, object_key, input_folder, input_file)
    else:
        print(f'Passed method {method_name} is not recorgnized!')
        sys.exit(1)

if __name__ == "__main__":
    # This ensures the script runs the main function when executed directly
    main()