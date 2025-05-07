import json
import boto3
import os
from collections import Counter
from typing import List
import re
from time import sleep

# Initialize S3 client
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

KEEP_KEY_VALUE_TEXT = CONFIG['keep-key-value-text']

def output_file_from_input(input_bucket: str, input_folder: str, input_file: str) -> List[str]:
    # Output bucket + folder are easy
    output_bucket = input_bucket
    output_folder = CONFIG['cleaned-data-folder']

    # Get output filename -- don't make this too hard
    output_file = input_file.replace(CONFIG['structured-extension'], CONFIG['cleaned-extension'])
    output_key = output_folder + output_file

    return output_bucket, output_key, output_folder, output_file

def lambda_handler(event, context):
    # EVENT: Textract output is structured into single json file, "ocr-results/" folder is added to
    
    # Extract bucket name and object key from the S3 event
    bucket, key, input_folder, input_file = utils.get_s3_paths(event)
    # Input file ex: Test123_Structured.json
    
    # Log process start
    utils.create_update_log_file(key=key, message="Data cleaning started", job_start=True)

    # Get output file destination and print
    output_bucket, output_key, output_folder, output_file = output_file_from_input(bucket, input_folder, input_file)
    print(f"Bucket Name: {bucket}, Input file: {input_file}, Output Bucket: {bucket}, Output Folder: {output_folder}")

    # Get JSON content from S3 file
    json_content = utils.load_s3_json(key=key, bucket=bucket)
    
    # Call the external clean_data function
    cleaned_data = clean_data(json_content)
    
    # Upload cleaned data to the output location in the same S3 bucket
    output_data = json.dumps(cleaned_data)
    s3.put_object(Bucket=output_bucket, Key=output_key, Body=output_data)
    
    # Log process start
    utils.create_update_log_file(key=key, message="Data cleaning finished", job_start=False)

    return{
        'statusCode': 200,
        'body': json.dumps(f"File '{key}' cleaned successfully, outputted to {output_key}")
    }
    
def clean_data(json_content: dict):
    # json_content is a dict mapping str(pagenum): page_text
    # Iterate through each cleaning function 
    output = json_content.copy()
    output = clean_json_page_keys(output)
    output = remove_excessive_whitespace(output)
    output = remove_headers_footers(output)

    # return when done
    return output

PATTERN = r'(Text:)(.*?)(\s*Key-Value.*)'
def get_before_middle_after(text: str) -> List[str]:
    match = re.search(PATTERN, text, re.DOTALL)
    # Match not found, return "" as before/after
    if match is None:
        return '', text, ''
    
    before, middle, after = match.groups()

    # Handle case where incoming text has no newlines, separated by commas
    if '\n' not in middle:
        middle = '\n'.join(middle.split(','))

    return before, middle, after

def recombine_before_middle_after(before: str, middle: str, after: str) -> str:
    if KEEP_KEY_VALUE_TEXT:
        return before + ' ' + middle + ' ' + after
    else:
        return middle

# region data cleaning functions

# Change JSON keys from "Page 1" to just "1"
def clean_json_page_keys(pages: dict) -> dict:
    output = {}
    for pagenum, page in pages.items():
        new_pagenum = pagenum.lower().replace('page', '').replace(' ', '')
        output[new_pagenum] = page
    return output

# Reduce sections with excessive "\n"
def remove_excessive_whitespace(pages, num_newlines_mid=3, num_newlines_end=1):
    output = pages.copy()
    for pagenum, page in output.items():
        sleep(0.04)
        before, middle, after = get_before_middle_after(page)
        if len(middle.strip()) != 0:
            while middle[-num_newlines_end] == '\n'*num_newlines_end:
                middle = middle[:-num_newlines_end]
        else:
            middle = " "
        middle = middle.replace('\n'*num_newlines_mid, '')
        output[pagenum] = recombine_before_middle_after(before, middle, after)
    return output

def remove_headers_footers(pages, top_n_lines=1, bottom_n_lines=1, threshold=0.6):
    headers, footers = detect_repeated_patterns(pages, top_n_lines=top_n_lines, bottom_n_lines=bottom_n_lines, threshold=threshold)
    cleaned_pages = pages.copy()
    count = 0
    while (headers is not None) or (footers is not None):
        if headers: print('Found headers:', headers)
        if footers: print('Found footers:', footers)

        for pagenum, page in cleaned_pages.items():
            # Split into before, middle, after
            before, middle, after = get_before_middle_after(page)

            # Split the page into lines
            page_lines = middle.splitlines() # list, split by line (\n or comma)

            # Remove header if present
            if headers:
                header_lines = headers.splitlines()
                if page_lines[:len(header_lines)] == header_lines:
                    page_lines = page_lines[len(header_lines):]

            # Remove footer if present
            if footers:
                footer_lines = footers.splitlines()
                if page_lines[-len(footer_lines):] == footer_lines:
                    page_lines = page_lines[:-len(footer_lines)]
            
            # Join the remaining lines back into a cleaned page
            new_text = '\n'.join(page_lines)
            cleaned_pages[pagenum] = recombine_before_middle_after(before, new_text, after) # sub PATTERN out for NEW_TEXT, keeping 1st and 3rd groups intact

        # After removing, see if there is another header/footer to remove
        headers, footers = detect_repeated_patterns(cleaned_pages, top_n_lines=top_n_lines, bottom_n_lines=bottom_n_lines, threshold=threshold)
        count += 1
        if count > 100: # failsafe
            break

    return cleaned_pages


# endregion

# region cleaning helpers
# Identify repeated header/footers
def detect_repeated_patterns(pages: dict, top_n_lines: int = 1, bottom_n_lines: int = 1, threshold: float = 0.6) -> List[str]:
    """
    Detects repeated patterns in the top and bottom n lines of each page (headers and footers).

    Args:
        pages (dict of str:str): The dict of raw text for each page of the document.
        top_n_lines (int): Number of lines from the top of each page to consider as potential headers.
        bottom_n_lines (int): Number of lines from the bottom of each page to consider as potential footers.
        threshold (float): The proportion of pages that must contain the same pattern to be considered a header/footer.

    Returns:
        headers (str): The most common header text.
        footers (str): The most common footer text.
    """
      # Below check takes care of the empty embedding issues for single page synthetic  data
    if len(pages) <= 1:
        return None, None
        
    top_lines = []
    bottom_lines = []

    # Extract top and bottom n lines from each page
    for page in pages.values():
        before, middle, after = get_before_middle_after(page)
        page_lines = middle.splitlines()

        # Top n lines (potential header)
        top_lines.append('\n'.join(page_lines[:top_n_lines]))

        # Bottom n lines (potential footer)
        bottom_lines.append('\n'.join(page_lines[-bottom_n_lines:]))

    # Count frequency of top and bottom lines
    top_counter = Counter(top_lines)
    bottom_counter = Counter(bottom_lines)

    # Determine most common headers and footers if they meet the threshold
    most_common_top, top_count = top_counter.most_common(1)[0]
    most_common_bottom, bottom_count = bottom_counter.most_common(1)[0]

    headers = most_common_top if top_count / len(pages) > threshold else None
    footers = most_common_bottom if bottom_count / len(pages) > threshold else None

    return headers, footers

# endregion

if __name__ == '__main__':
    file = 'Test456_Structured.txt'

    event = {
        'Records':[{
            's3': {
                'bucket': {'name': 'ahrq-qsrs-ml-poc'},
                'object': {'key': 'structured-data/'+file}
            }
        }]
    }
    
    response = lambda_handler(event, None)
    print(response)