import boto3
import json

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

# Get config file
CONFIG = utils.get_config()

def lambda_handler(event, context):
    # EVENT: called to answer a question from the LLM
    print(event)

    # Step 1: Access the payload sent from initiating Lambda
    prompt, pretty_prompt = get_prompt_from_event(event)

    algorithm = event.get('algorithm') # not required yet
    all_page_text_file = event['all_page_text_file']
    all_page_text = utils.load_s3_json(folder=CONFIG['cleaned-data-folder'], file=all_page_text_file, bucket=CONFIG['bucket'], json_key=None)
    embeddings_key = event['embeddings_key']
    embeddings = utils.load_s3_json(key=embeddings_key, bucket=CONFIG['bucket'], json_key=None)
            
    # Step 1.5 -- splice out just question from prompt artifacts?
    # Prompt artifacts: "Answer in MM/DD/YYYY format" or "Choose from one of these options: Yes/No/Can't tell"
    question = prompt.split('|')[0]

    # Step 2: Vector-embed the question and compute cosine similarities
    question_embeddings_1d = utils.query_embeddings_endpoint(question) # may replace with "question" if doing step 3.5
    similarities = {pagenum: utils.cosine_similarity(question_embeddings_1d, page_embedding) for pagenum, page_embedding in embeddings.items()}

    # Step 3: Construct prompt minus context
    prompt_minus_context = utils.construct_prompt_minus_context(prompt)

    # Step 4: Recursively query LLM with fewer pages of context until we are under the token limit
    answer_plus_reason, pages_used, confidence_score = utils.query_llm(
        prompt_minus_context=prompt_minus_context,
        similarities_dict=similarities,
        all_page_text=all_page_text,
        context_replace=CONFIG['context-replace']
    )

    # Step 5: Split answer & reason, store in output
    answer, reason = utils.parse_answer_and_reason(answer_plus_reason)
    output = {
        'Question': pretty_prompt, # may replace "prompt" with "question" variable if doing step 1.5
        'Answer': answer,
        'Reason': reason,
        'Pages used': pages_used,
        'Confidence score': confidence_score
    }

    return json.dumps(output)


def get_prompt_from_event(event):
    base_prompt = event['prompt']
    prompt, pretty_prompt = handle_list_replace_prompt(event, base_prompt)
    return prompt, pretty_prompt


# A list-replace question, e.g. "Which of the following blood products did the patient receive: {product-list}?"
def handle_list_replace_prompt(event, prompt):
    if '{' in prompt and '-list}' in prompt:
        config_questions_key = event['config_questions_key']
        qnum = event['qnum']

        word_replace = CONFIG[config_questions_key][f'{qnum}-word-replace']
        lst = ', '.join(CONFIG[config_questions_key][f'{qnum}-list'])
        prompt = prompt.replace(word_replace, lst)

        pretty_prompt = CONFIG[config_questions_key][f'{qnum}-pretty']
    else:
        pretty_prompt = prompt
    
    return prompt, pretty_prompt