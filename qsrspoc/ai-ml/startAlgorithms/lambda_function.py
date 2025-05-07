import json
import boto3
import time
s3 = boto3.client('s3')
stepfunctions_client = boto3.client("stepfunctions")
# Get utils - 1
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
MAX_CONCURRENT_EXECUTIONS = 2

def get_running_executions(step_function_ARN):
    """Returns the number of currently running Step Function executions."""
    response = stepfunctions_client.list_executions(
        stateMachineArn=step_function_ARN,
        statusFilter="RUNNING"
    )
    return len(response.get("executions", []))

def lambda_handler(event, context):
    # EVENT: page-embeddings folder is added to

    # Process a single event
    record = event["Records"][0]
    s3_key = record["s3"]["object"]["key"]
    arn = CONFIG['main-algorithm-orchestrator-SF-arn']
    print(f"Processing file: {s3_key}")
    
    # Wait until there are less than 2 active executions running
    while get_running_executions(arn) >= MAX_CONCURRENT_EXECUTIONS:
        print("Waiting for execution slot...")
        time.sleep(10)  # Wait for 10 seconds before checking again

    # Step 1: Extract S3 bucket and file information from the event
    bucket, key, input_folder, input_file = utils.get_s3_paths(event)

    # Step 2: Set up a new template file to hold data passed between step functions for this embedded file
    utils.create_initialize_data_passing_file(page_embeddings_key=key)
    
    # Step 3: Start the "MainAlgorithmOrchestrator" step-function  
    stepfunctions_client.start_execution(
        stateMachineArn=arn,
        input=json.dumps({"Records": event["Records"]})
    )

    # Log start of LLM process
    utils.create_update_log_file(key=key, message="LLM output process started", job_start=True)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'"MainAlgorithmOrchestrator" step-function started successfully',
        })
    }

if __name__ == '__main__':
    file = '4928968_Redacted_embeddings.json'

    event = {
        'Records':[{
            's3': {
                'bucket': {'name': 'ahrq-qsrs-ml-poc'},
                'object': {'key': 'ai-ml/page-embeddings/'+file}
            }
        }]
    }

    response = lambda_handler(event, None)
    print(response)