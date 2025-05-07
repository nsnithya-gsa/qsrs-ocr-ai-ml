import math
import json
import re
import urllib
from datetime import datetime

import boto3
import botocore

from typing import Union, List, Tuple
		 

s3 = boto3.client('s3')

# Get config file
def get_bucket() -> str:
    x = boto3.resource('s3').Bucket('ahrq-qsrs-ml-poc')
    if x.creation_date is not None:
        return 'ahrq-qsrs-ml-poc'
    return None

def get_config() -> dict:
    response = s3.get_object(Bucket='ahrq-qsrs-ml-poc', Key='config/ai-ml/config.json')
    data = response['Body'].read().decode('utf-8')
    config = json.loads(data, strict=False)
    return config

CONFIG = get_config()

BUCKET = CONFIG['bucket']

sagemaker_endpoint = CONFIG['sagemaker-endpoint']

# region S3 pathing and loading files
def check_file_exists(folder: str = None, file: str = None, key: str = None, bucket: str = BUCKET) -> bool:

    assert (folder is not None and file is not None) or (key is not None), 'Must specify either (folder+file) or key!'
    
    # Derive key from folder + file
    if key is None:
        if not folder.endswith('/'): folder = folder + '/'
        key = folder + file

    # Don't raise any errors, just T/F
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except Exception as e:
        return False

def get_s3_paths(event) -> List[str]:

    # Extract bucket name and object key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    *input_folders, input_file = object_key.split('/')
    if len(input_folders) == 1: input_folders = input_folders[0]

    return bucket_name, object_key, input_folders, input_file

def load_s3_json(
    folder: str = None,
    file: str = None,
    key: str = None,
    bucket: str = BUCKET,
    json_key: Union[str, List[str]] = None
) -> dict:
	
    assert (folder is not None and file is not None) or (key is not None), f'Must specify either (folder+file) or key!\n {folder} {file} | {key}'
    
    # Derive key from folder + file
    if key is None:
        if not folder.endswith('/'): folder = folder + '/'
        key = folder + file
    
    # Download the file from the S3 bucket
    input_obj = s3.get_object(Bucket=bucket, Key=key)

    # Parse the json response
    json_content = json_response_to_dict(input_obj, json_key=json_key)

    return json_content

def json_response_to_dict(json_response: dict, json_key: Union[str, List[str]] = None) -> dict:
	
    # Read body and decode
    input_data = json_response['Body'].read().decode('utf-8')
        
    # Parse the JSON content
    json_content = json.loads(input_data, strict=False)
    if json_key is not None:

        # Handle multiple layers of keys
        if isinstance(json_key, List):
            for k in json_key:
                json_content = json_content[k]

        # Handle single string layer
        else:
            json_content = json_content[json_key]

    return json_content

def get_llm_output_filename(page_embeddings_file: str) -> str:
    # Replace the page embeddings extension with the llm output extension
    output = page_embeddings_file.replace(CONFIG['embeddings-extension'], CONFIG['llm-output-extension'])
    
    return output

def download_existing_llm_output(page_embeddings_file: str, llm_output_folder: str = CONFIG['llm-output-folder']) -> dict:
    # Convert input page-embeddings file into location of final llm output
    output_file = get_llm_output_filename(page_embeddings_file)

    # If output file doesn't exist, return empty dict
    if not check_file_exists(folder=llm_output_folder, file=output_file):
        return {}
    
    # If file exists, download it and return
    json_data = load_s3_json(folder=llm_output_folder, file=output_file, json_key=None)
    return json_data


def upload_llm_output(output_json: dict, page_embeddings_file: str, llm_output_folder: str = CONFIG['llm-output-folder']) -> None:
    # Convert input page-embeddings file into location of final llm output
    output_file = get_llm_output_filename(page_embeddings_file)

    # Add the provided json dict to the file
    s3.put_object(
        Bucket=BUCKET, # hardcode this???
        Key=llm_output_folder+output_file,
        Body=json.dumps(output_json)
    )


# endregion

# region embeddings
def get_current_pagenum(pgnum: str) -> int:
    # Input pagenum, like "1" or "Page 1"
    # Output int of that
    x = pgnum.lower().replace('page', '')
    try:
        return int(x)
    except:
        print(f'Cannot coerce pgnum "{pgnum}" to int')
        return 0

def get_max_pagenum(text_data: dict) -> int:
    return max([get_current_pagenum(pgnum) for pgnum in text_data.keys()])

def query_embeddings_endpoint(text: str):
    # Is this best practices?
    sagemaker_runtime = boto3.client('runtime.sagemaker', region_name='us-east-1')

    # Prepare payload for SageMaker endpoint
    payload = json.dumps({"inputs": text})
    
    # Send the request to the SageMaker endpoint
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=sagemaker_endpoint,
        ContentType='application/json',
        Body=payload
    )
    
    # Parse the response
    embeddings_1d = json_response_to_dict(response, json_key=['predictions', 'embeddings'])

    return embeddings_1d

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes the cosine similarity between two vectors.

    Args:
    - vec1 (list of float): First vector.
    - vec2 (list of float): Second vector.

    Returns:
    - float: Cosine similarity between vec1 and vec2.
    """
    # Ensure the vectors have the same length
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must be of the same length")

    # Compute the dot product of the two vectors
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))

    # Compute the magnitudes of the vectors
    magnitude_vec1 = math.sqrt(sum(v1 ** 2 for v1 in vec1))
    magnitude_vec2 = math.sqrt(sum(v2 ** 2 for v2 in vec2))

    # Avoid division by zero
    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0.0

    # Compute and return cosine similarity
    return dot_product / (magnitude_vec1 * magnitude_vec2)

def compute_similarity_weighted_confidence(similarity_scores):
    weights = [score ** 2 for score in similarity_scores]  # Square the similarity scores
    weighted_score = sum(w * s for w, s in zip(weights, similarity_scores)) / sum(weights)
    return weighted_score
# endregion

# region step functions
def construct_stepfunction_input(**kwargs):
    DEFAULT_FILE = CONFIG['default-file']
    DEFAULT_ALGORITHM = CONFIG['default-algorithm']
    DEFAULT_BUCKET = CONFIG['bucket']


    # Fill in missing kwargs with defaults
    s3_like_input = json.dumps({
        "Records": [{
            "s3": {
                "bucket": {"name": kwargs.get('bucket', DEFAULT_BUCKET)},
                "object": {"key": f"ai-ml/page-embeddings/{kwargs.get('file', DEFAULT_FILE)}"}
            }
        }],
        "algorithm": kwargs.get('algorithm', DEFAULT_ALGORITHM)
    })

    return s3_like_input

# this is called by the startAlgorithm lambda before triggering the Main Algorithm Orchestrator
# each MAO execution on the same embedded file will overwrite data from the last execution for that file
def create_initialize_data_passing_file(page_embeddings_key: str,  bucket: str = BUCKET) -> None:

    # set up s3 key (folder path plus filename) for the file to later store passed data
    data_passing_key = (
        page_embeddings_key.replace(CONFIG["embeddings-folder"], CONFIG["passed-step-function-data-folder"])
            .replace(CONFIG["embeddings-extension"], CONFIG["passed-data-extension"])
    )

    # retrieve the template dict from code/data_passing_structure.json
    passed_data_template_bucket = CONFIG['bucket']
    passed_data_template_folder = 'ai-ml/code/'
    passed_data_template_filename = 'data_passing_structure.json'

    # Load template file
    template_dict = load_s3_json(folder=passed_data_template_folder, file=passed_data_template_filename, bucket=passed_data_template_bucket, json_key=None)
   
    # if the file already exists, overwrite it with a fresh template
    s3.put_object(
        Bucket=bucket,
        Key=data_passing_key,
        Body=json.dumps(template_dict, indent=4),
        ContentType="application/json"
    )

# TODO: remove redundancies with related data passing utils by splitting into smaller function units
def retrieve_data_passing_file(page_embeddings_key: str,  bucket: str = BUCKET) -> None:

    # set up s3 key for file to retrieve
    data_passing_key = (
        page_embeddings_key.replace(CONFIG["embeddings-folder"], CONFIG["passed-step-function-data-folder"])
            .replace(CONFIG["embeddings-extension"], CONFIG["passed-data-extension"])
    )

    # retrieve the data passing file; if no file exists (ex: non-MAO test algorithm execution)
    # it will be created from the template
    try:
        input_obj = s3.get_object(Bucket=bucket, Key=data_passing_key)
        json_content = json.loads(input_obj["Body"].read().decode("utf-8"))
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            # File doesn't exist, create it with the template
            # retrieve the template dict from code/data_passing_structure.json
            passed_data_template_bucket = CONFIG['bucket']
            passed_data_template_folder = 'ai-ml/code/'
            passed_data_template_filename = 'data_passing_structure.json'

             # Load template file
            template_dict = load_s3_json(folder=passed_data_template_folder, file=passed_data_template_filename, bucket=passed_data_template_bucket, json_key=None)
   
            s3.put_object(
                Bucket=bucket,
                Key=data_passing_key,
                Body=json.dumps(template_dict, indent=4),
                ContentType="application/json"
            )
            return template_dict  # Return template dict since we just created the file
        else:
            raise  # Re-raise other unexpected errors

    return json_content


def download_existing_data_passing_file(page_embeddings_file: str, data_passing_folder: str = CONFIG['passed-step-function-data-folder']) -> dict:                                        
    output_file = page_embeddings_file.replace(CONFIG['embeddings-extension'], CONFIG['passed-data-extension'])
    # If output file doesn't exist, return empty dict

    if not check_file_exists(folder=data_passing_folder, file=output_file):
        return {}
    
    # If file exists, download it and return
    json_data = load_s3_json(folder=data_passing_folder, file=output_file, json_key=None)
    return json_data

def upload_passed_data_json(passed_data_json: dict, page_embeddings_file: str, passed_data_folder: str = CONFIG['passed-step-function-data-folder']) -> None:
    output_file = page_embeddings_file.replace(CONFIG['embeddings-extension'], CONFIG['passed-data-extension'])

    # Add the provided json dict to the file
    s3.put_object(
        Bucket=BUCKET, # hardcode this???
        Key=passed_data_folder+output_file,
        Body=json.dumps(passed_data_json)
    )


# endregion

# region preparing to query LLM
def load_questions(algorithm: str = None) -> dict:
    # Establish paths
    questions_bucket = CONFIG['bucket']
    questions_folder = 'ai-ml/code/'
    questions_filename = 'prompts.json'

    # Load file and parse response
    questions = load_s3_json(folder=questions_folder, file=questions_filename, bucket=questions_bucket, json_key=None)

    # Return full dict, or specific algorithm from that dict
    if algorithm is None: return questions
    return questions.get(algorithm)

def get_matching_pdf_text(
    page_embeddings_file: str,
    s3_bucket: str = BUCKET,
    s3_folder: str = CONFIG['cleaned-data-folder'],
    cleaned_extension: str = CONFIG['cleaned-extension']
) -> dict:
    # Get the name of the file holding the cleaned PDF text file
    page_embeddings_file_nofolder = page_embeddings_file.split('/')[-1]
    pdf_text_file_name = get_matching_pdf_text_FILE(page_embeddings_file_nofolder, s3_bucket=s3_bucket, s3_folder=s3_folder, cleaned_extension=cleaned_extension)

    # Load the file from s3 and parse JSON response
    text_data = load_s3_json(folder=s3_folder, file=pdf_text_file_name, bucket=s3_bucket, json_key=None)

    # Return
    return text_data

def get_matching_pdf_text_FILE(
    page_embeddings_file: str,
    s3_bucket: str = BUCKET,
    s3_folder: str = CONFIG['cleaned-data-folder'],
    cleaned_extension: str = CONFIG['cleaned-extension']
) -> str:
    """
    Get file from specified s3 bucket and folder (post-ocr cleaned) that matches the 
    filename signature of (the file containing the vector embeddings per page here)

    Output: str filename
    """
    # Extract root file from input file
    page_embeddings_file = page_embeddings_file.split('/')[-1]
    
    # Get expected "cleaned" filename from page-embeddings filename
    expected_cleaned_filename = page_embeddings_file.replace(CONFIG['embeddings-extension'], CONFIG['cleaned-extension'])
    if not check_file_exists(folder=s3_folder, file=expected_cleaned_filename):
        raise ValueError(f'Expected matching file "{expected_cleaned_filename}" not found in folder "{s3_folder}" for bucket "{s3_bucket}"')
    
    return expected_cleaned_filename


DELIMITER = CONFIG['delimiter']
def construct_prompt_minus_context(question: str) -> str:
    prompt_template = """Answer the following QUESTION based on the CONTEXT given. Assume that the provided
    CONTEXT is the most relevant information from this hospitalization event. If the CONTEXT shows no evidence
    of the key element of the question, assume the element was absent. Provide the answer, followed by the "{delimiter}"
    delimiter and a single sentence explaining how you know. Follow all question-specific formatting instructions carefully. 
    Some multiple choice questions may ask you to respond with "other" if a relevant item is not listed.If the QUESTION directs 
    you to respond with yes/no/can't tell, use this rule about answering "no" vs answering "can't tell": if no information directly 
    related to the question is present in the CONTEXT, answer "no" and if information directly related to the question is present 
    in the CONTEXT but insufficient to respond with "yes", answer "can't tell. When reasoning about time or dates, ensure chronological 
    accuracy—clearly identify which event came first, and avoid contradictions or repetition when comparing dates or time spans to 
    generate your answer."

    QUESTION:
    {question}

    CONTEXT:
    {context}
    """

    prompt_minus_context = prompt_template.replace('{question}', question).replace('{delimiter}', DELIMITER)
    return prompt_minus_context

# endregion

# region querying LLLM
def query_llm(
    prompt_minus_context: str,
    similarities_dict: dict,
    all_page_text: dict,
    context_replace: str = '{context}',
    num_pages: int = 8,
    prnt: bool = True
) -> Tuple[str, List]:
    # Recursion stop gate
    if num_pages == 0:
        raise ValueError('Cannot answer the question with 0 pages of context!')
    
    # Try to query with this much context
    try:
        # Sort best pages down to worst pages
        best_pages_sorted = sorted(similarities_dict.keys(), key=lambda k: similarities_dict[k], reverse=True)
        pages_used = best_pages_sorted[:num_pages]

        # get the similarity scores for the pages used and generate a confidence metric based on them
        scores_for_used_pages = [similarities_dict[page] for page in pages_used if page in similarities_dict]
        weighted_aggregate_page_confidence = compute_similarity_weighted_confidence(scores_for_used_pages)

        pages_used_starts_from_1 = [int(p) - int(min(best_pages_sorted))+1 for p in pages_used] # e.g. [-1, 0, 1, ...] --> [1, 2, 3, ...]
        print(best_pages_sorted[:10])

        # Get N pages of context from similarities dict
        context = '\n---PAGE BREAK---\n'.join([
            all_page_text[pagenum] for pagenum in pages_used
        ])

        # Populate prompt with context
        prompt = prompt_minus_context.replace(context_replace, context)

        # Query LLM and return
        answer_plus_reason = query_llm_helper(prompt)
        return answer_plus_reason, pages_used_starts_from_1, weighted_aggregate_page_confidence

    except Exception as e:
        
        e_str = str(e).lower()
        # Check if the error is related to the input text being too long (too many tokens)
        if ("model's maximum context length" in e_str) and ("please reduce the length of the prompt" in e_str):
            if prnt: print(f"Context may be too long with {num_pages} pages, trying next with {num_pages-1} pages.")

            # Try again with one less page of context
            return query_llm(prompt_minus_context, similarities_dict=similarities_dict, all_page_text=all_page_text,
                             context_replace=context_replace, num_pages=num_pages-1, prnt=prnt)
        
        else:
            # For other exceptions, raise the error
            raise

def query_llm_helper(prompt: str, model_id: str = CONFIG['model-id']) -> str:
    bedrock = boto3.client('bedrock-runtime')
    # Input: long text string
    # Output: response text from the LLM
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]
    
    # Send the message to the model, using a basic inference configuration.
    response = bedrock.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens":2048,"temperature":0.3,"topP":0.9},
        additionalModelRequestFields={},
    )

    # body = json.dumps({'prompt': prompt})
    # response = bedrock.invoke_model(
    #     modelId = model_id,
    #     body=body,
    #     contentType='application/json'
    # )


    # Extract and return the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    return response_text

def invoke_querying_lambda(
    prompt: str,
    all_page_text_file: str,
    embeddings_key: str,
    algorithm: str = None,
    asynchronous: bool = False
) -> dict:
    
    lambda_client = boto3.client('lambda')

    # Prepare payload to invoke
    FUNCTION_NAME = 'answerQuestion'
    payload = {
        'prompt': prompt,
        'algorithm': algorithm,
        'all_page_text_file': all_page_text_file,
        'embeddings_key': embeddings_key,
    }

    try:
        # Invoke the lambda, sync or async
        response = lambda_client.invoke(
            FunctionName = FUNCTION_NAME,
            InvocationType=('Event') if asynchronous else ('RequestResponse'),
            Payload = json.dumps(payload)
        )

        # Read the response payload and decode it
        response_payload = response['Payload'].read().decode('utf-8')
        result = json.loads(response_payload) # dict with keys: ["Question", "Answer", "Reason"]
        while isinstance(result, str): # sometimes need to call json.loads twice???
            result = json.loads(result)
        print(result)
        print()

        return result
    
    except Exception as e:
        print('Error invoking the query lambda!')
        print('Algorithm:', algorithm)
        print('Prompt:', prompt)
        print('Error:', str(e))
        raise

def empty_response():
    return {'Question': '', 'Answer': '', 'Reason': '', 'Pages used': [], 'Confidence score': ''}
# endregion

# region postprocessing LLM response
def parse_answer_and_reason(response: str) -> List[str]:
    # Check if response is delimited
    if DELIMITER not in response:
        print(f'Delimiter "{DELIMITER}" not present -- cannot identify where answer stops and reason begins!')
        print('Response:')
        print(response)
        print('END RESPONSE')
        return clean_answer(response), ''
    
    # If so, split based on delimiter and return
    response_split = response.split(DELIMITER)
    if len(response_split) != 2: # answer / reason
        print(f'Delimiter "{DELIMITER}" present {len(response_split)-1} times -- cannot identify where answer stops and reason begins!')
        print('Assuming first occurrence of delimiter is where answer stops')
        print('Response:')
        print(response)
        print('END RESPONSE')
        return clean_answer(response_split[0]), '\n'.join(response_split[1:])
    
    else:
        answer, reason = response_split
        return clean_answer(answer), reason
    
def clean_answer(answer: str) -> str:
    x = answer.lower().replace('answer', '')
    x = x.replace('\n', '')
    x = x.replace(':', '')
    x = x.replace('None', '')
    x = x.strip() # clear whitespace from front and back -- always last step
    return x

def explicit_yes(response: Union[str, dict]) -> bool:
    if isinstance(response, dict):
        return explicit_yes(response['Answer'])
    return response.lower().strip() in ['y', 'yes']

def explicit_no(response: Union[str, dict]) -> bool:
    if isinstance(response, dict):
        return explicit_no(response['Answer'])
    return response.lower().strip() in ['n', 'no']
# endregion


# region logging
def create_update_log_file(key: str, message: str, job_start: bool, bucket: str = BUCKET, **kwargs) -> None:
    # Specify log file location
    log_prefix = CONFIG['logPrefix']
    logfile_key = f"{log_prefix}{datetime.now().strftime('%m%Y')}.json"

    # Print out details
    try:
        file_size = s3.head_object(Bucket=bucket, Key=key)['ContentLength']
    except:
        file_size = -1
    print(f'bucket name : {bucket}, object key: {key}, file size: {file_size}')
   
    # File content
    body = {
        "bucketname": bucket,
        "filepath": key,
        "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "filesize": file_size,
        "pagecount": "NA",
        "status": ("Started") if job_start else ("Ended"),
        "message": message
    }
    body.update(kwargs)
    
    # If file exists, download and append; else, create new output
    if check_file_exists(key=logfile_key, bucket=bucket):
        log_data = load_s3_json(key=logfile_key, bucket=bucket, json_key=None)
        log_data.append(body)
    else:
        log_data = [body]
    
    # Upload log data
    s3.put_object(
        Bucket=bucket,
        Key=logfile_key,
        Body=json.dumps(log_data)
    )
# endregion