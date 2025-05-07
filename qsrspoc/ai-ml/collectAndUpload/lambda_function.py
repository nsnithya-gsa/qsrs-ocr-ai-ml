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
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# E.g. HAI-COVID-19 algorithm -- make separate scripts for each algorithm?
# If so, can implement algorithm flow here ("If Q2 is NO, exit, else move onto Q3")
# If not, just ask/answer every question, and leave algorithm flow for somewhere else

# For now, implement HAI-COVID-19

def lambda_handler(event, context):
    
    # Step 1: Access payload sent by initiating step function
    page_embeddings_key = event['page-embeddings-file']
    page_embeddings_file = page_embeddings_key.split('/')[-1]
    algorithm = event['algorithm']
    passed_data = event['passed_data']

    # Step 2: Get prompt-keys for this specific algorithm
    prompts = utils.load_questions(algorithm=algorithm)

    # Step 3: Look for responses to each question, else fill with empty response
    output = {}
    num_questions = 0
    for prompt_key in prompts.keys():
        resp = event.get(prompt_key)
        if resp is None or resp == '':
            output[prompt_key] = utils.empty_response()
        else:
            output[prompt_key] = resp
            num_questions += 1

    # Step 4: Download output JSON, add this into it, and re-upload
    already_existing_output_json = utils.download_existing_llm_output(page_embeddings_file=page_embeddings_file)
    already_existing_output_json[algorithm] = output.copy()
    utils.upload_llm_output(already_existing_output_json, page_embeddings_file=page_embeddings_file)
    
    # Step 5: Download passed_data JSON, overwrite it with the new blob, and re-upload
    already_existing_passed_data_json = utils.download_existing_data_passing_file(page_embeddings_file=page_embeddings_file)
    already_existing_passed_data_json = passed_data.copy()
    utils.upload_passed_data_json(already_existing_passed_data_json, page_embeddings_file=page_embeddings_file)

    # Log process end
    #utils.create_update_log_file(key=page_embeddings_key, message=f"Algorithm {algorithm} finished", job_start=False, num_questions=num_questions)

    # end
    response = {
        'statusCode': 200,
        "body": json.dumps({
            'message': f'{algorithm} collected and uploaded successfully for file: {page_embeddings_file}'
        })
    }
    # if algorithm is Exit, log that AIML portion is done
    if algorithm == "Exit":
        logger.info(f"LLM output process finished")
        utils.create_update_log_file(key=page_embeddings_key, message="LLM output process finished", job_start=False)
    return response