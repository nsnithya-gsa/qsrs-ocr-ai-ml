import json
import boto3
import os
from typing import List
import time

s3 = boto3.client('s3')
batch_client = boto3.client('batch')

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

# Get config file
CONFIG = utils.get_config()
#Get output file based on the input file
def output_file_from_input(input_bucket: str, input_folder: str, input_file: str) -> List[str]:
    # Output bucket + folder are easy
    output_bucket = input_bucket
    output_folder = CONFIG['embeddings-folder']
    
    ### Get output filename
    output_file = input_file.replace(CONFIG['cleaned-extension'], CONFIG['embeddings-extension'])

    output_key = output_folder + output_file

    return output_bucket, output_key, output_folder, output_file

def lambda_handler(event, context):
    import time
    t1 = time.time()
    # EVENT: textract text output is cleaned, "cleaned" folder is added to

    # Step 1: Extract S3 bucket and file information from the event
    bucket, key, input_folder, input_file = utils.get_s3_paths(event)
    # Input file ex: Test123_datetime_HASH.json
    
    #get config value to verify if needed to call AWS Batch job
    send_to_batch = CONFIG['embeddings_send_to_batch']
    #Check the value of send_to_batch, if "1" submit AWS Batch job
    if send_to_batch == '1':
        print(f'Send to Batch')
        batch_methodname = CONFIG['batch_methodname']
        batch_jobname = CONFIG['batch_jobname']
        batch_jobqueue = CONFIG['batch_jobqueue']
        batch_jobdefinition = CONFIG['batch_jobdefinition']
        batch_pythoncodefile = CONFIG['batch_pythoncodefile']
        
        response = batch_client.submit_job(
        jobName=batch_jobname,
        jobQueue=batch_jobqueue,  #Replace with your Batch Job Queue
        jobDefinition=batch_jobdefinition,  #Replace with your Batch Job Definition
        containerOverrides={
            'command': ['python','awsbatch_page_embeddings_job.py', batch_methodname, bucket, key, input_folder, input_file]
        }
        )
    else:
        # Step 1.5: Log process start
        utils.create_update_log_file(key=key, message="Page embeddings started", job_start=True)
        
        # Step 2: Download the text file from S3
        text_data = utils.load_s3_json(key=key, bucket=bucket, json_key=None)
        
        # Step 3: Call SageMaker Endpoint to get embeddings, once per page
        embeddings_1d = {} # dict like {str: (768,) }
        for pagenum, page in text_data.items(): 
            print(utils.get_current_pagenum(pagenum), '/', utils.get_max_pagenum(text_data))
            embeddings_1d[pagenum] = utils.query_embeddings_endpoint(page)
        
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

        # Log start of LLM process
        time.sleep(1.1)
        utils.create_update_log_file(key=key, message="LLM output process started", job_start=True)

        t2 = time.time()
        print(f'This took {t2-t1:.2f} seconds')
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Embeddings generated and saved to S3.',
                'output_file': output_key
            })
        }




if __name__ == '__main__':
    #file = 'Test122_20240927123416_81a9c178a4bd55853f58849a807adbb8e369e62419b8dee33cdb232984f2576c_cleaned.json'
    #file = '4927802_Redacted_cleaned.json'
    #file = '4927915_Redacted_cleaned.json'
    #file = '4928092_Redacted_cleaned.json'
    #file = '4928314_Redacted_cleaned.json'
    #file = '4928347_Redacted_cleaned.json'

    #file = '4928407_Redacted_cleaned.json'
    #file = '4928489_Redacted_cleaned.json'
    #file = '4928968_Redacted_cleaned.json'
    file = '4929111_Redacted_cleaned.json'
    print(file)

    event = {
        'Records':[{
            's3': {
                'bucket': {'name': 'ahrq-qsrs-ml-poc'},
                'object': {'key': 'cleaned-data/'+file}
            }
        }]
    }
    
    response = lambda_handler(event, None)
    print(response)