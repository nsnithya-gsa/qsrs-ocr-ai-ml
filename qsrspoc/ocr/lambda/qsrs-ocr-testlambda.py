import json
import boto3
import urllib.parse
import time
import os
import re  

# Initialize boto3 clients for Textract and S3
textract = boto3.client('textract')
s3 = boto3.client('s3')
sns_client = boto3.client('sns')


def lambda_handler(event, context):
    try:
        # Loop through each record (message) in the SQS event
        
        #build_structured_and_segmented_data()
        #build_segmented_data_simple_structure()
        trigger_AWS_batch()
            
        return {
            'statusCode': 200,
            'body': json.dumps('Processing completed successfully')
        }

    except Exception as e:
        print(f"Error processing Textract job result: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing Textract job result: {e}")
        }
def trigger_AWS_batch():
    method_name = 'process_textract_job'
    job_id = '8e16510ef7c74b4dd71f095e37c6c5e2f9a4fc7c6baa5b0e62aba7e9336aba6f'
    output_bucket='ahrq-qsrs-ml-poc'
    output_key = 'ocr-results/Test456_ocrresults.json'
    response = batch_client.submit_job(
        jobName='qsrs-ocr-awsbatch-job',
        jobQueue='qsrs-ocr-job-queue-awsbatch',  #Replace with your Batch Job Queue
        jobDefinition='qsrs-ocr-job-awsbatch',  #Replace with your Batch Job Definition
        containerOverrides={
            'command': ['python','awsbatch_job.py', method_name, job_id, output_bucket, output_key]
        }
        )
    print(f"Trigger to AWS Batch '{job_id}' Method Name '{method_name}' with object path '{output_key}'")
    
def build_structured_and_segmented_data():
    bucket_name = 'qsrs-ocr-poc-dev'
    file_key = 'ocr-results/4928968_Redacted_20241001-173934_6ad9b339c505ef409abc0b3e20f367c40426f5baf615f02205d47bd69a33276b.json'
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    # Read the content of the object (file)
    content = response['Body'].read().decode('utf-8')
    
    # Parse the JSON content
    json_data = json.loads(content)
    outformat = os.getenv('filestructure')
    
    print(f'response_json: {json_data}')
    
    #structured_output = extract_sections_by_page(json_data)
    structured_output = extract_text_from_textract_withoutsection(json_data)
   
    key_to_find_coversheet = "Clinical Data Abstraction Center Medical Record Coversheet"
    coversheet_instance_count = count_text_across_pages(structured_output, key_to_find_coversheet) 
    print(f'{coversheet_instance_count}')
    output_string = build_output_string_withoutsection(structured_output,coversheet_instance_count)
    
    #comprehend_input = json.dumps({"text": formatted_text})
    key_to_find_caseid = "CMS Control Number"
    case_id = find_key_value_in_string(output_string, key_to_find_caseid)
    key_to_find_instanceid = "Instance ID"
    instance_id = find_key_value_in_string(output_string, key_to_find_instanceid)
    key_to_find_coversheet = "Clinical Data Abstraction Center Medical Record Coversheet"
    instance_id = find_key_value_in_string(output_string, key_to_find_coversheet)
    print(f'Case ID: {case_id}, instance ID: {instance_id}')
    cleanpdf_output_key = f'structured-data/4928968_Redacted_structured.txt'
    # Upload the results to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=cleanpdf_output_key,
        Body=output_string
    )
    datachunking = os.getenv('datachunking')
    
    if datachunking == '1':
        chunks = chunk_text_by_page(output_string)
        for i, chunk in enumerate(chunks, 1):
            file_name = f'data-segments/4928968_Redacted_chunks/4928968_Redacted_chunk_{i}.txt'
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=chunk)
    

def extract_sections_by_page(textract_json):
    blocks = textract_json.get('Blocks', [])
    
    structured_data = {}

    # Block ID to Block mapping for fast lookup
    block_by_id = {block['Id']: block for block in blocks}

    for block in blocks:
        page_number = block.get('Page', 1)
        
        # Initialize structure for each page
        if page_number not in structured_data:
            structured_data[page_number] = {
                'Sections': []
            }

        block_type = block.get('BlockType')
        text = block.get('Text', '')
        geometry = block.get('Geometry', {}).get('BoundingBox', {})
        left_position = geometry.get('Left', 1)

        # Detect section headers and subsections
        if is_section_header(text, left_position):
            structured_data[page_number]['Sections'].append({
                'SectionHeader': text,
                'LeftPosition': left_position,  # Store left position
                'Text': [],
                'KeyValuePairs': [],
                'Tables': {}
            })

        # Handle LINE blocks (text)
        if block_type == 'LINE':
            if structured_data[page_number]['Sections']:
                last_section = structured_data[page_number]['Sections'][-1]
                last_section['Text'].append(text)

        # Detect key-value pairs (forms)
        elif block_type == 'KEY_VALUE_SET':
            key, value = extract_key_value_pair(block, block_by_id)
            if structured_data[page_number]['Sections']:
                last_section = structured_data[page_number]['Sections'][-1]
                if key.strip().endswith(':'):
                    key = key.rstrip(':')
                    key = key.replace(':','')
                if key != '' or value != '':
                    last_section['KeyValuePairs'].append({key: value})

        # Detect table blocks
        elif block_type == 'TABLE':
            table_data = extract_table_data(block, block_by_id)
            if structured_data[page_number]['Sections']:
                last_section = structured_data[page_number]['Sections'][-1]
                table_id = f"Table{len(last_section['Tables']) + 1}"
                last_section['Tables'][table_id] = table_data

    return structured_data

def replace_in_dict(d, old, new):
    for key, value in d.items():
        if isinstance(value, dict):
            # Recursively handle nested dictionaries
            replace_in_dict(value, old, new)
        elif isinstance(value, str):
            # Replace string values
            d[key] = value.replace(old, new)


def extract_text_from_textract_withoutsection(textract_json):
    blocks = textract_json.get('Blocks', [])
    
    # Dictionaries to store structured data for each page
    page_content = {}
    
    # Store blocks by their ID for faster lookup
    block_by_id = {block['Id']: block for block in blocks}

    for block in blocks:
        block_type = block.get('BlockType')
        page_number = block.get('Page', 1)
        
        # Initialize page entry if not already present
        if page_number not in page_content:
            page_content[page_number] = {
                'KeyValuePairs': [],
                'text': [],
                'tables': []
            }

        # Handle KEY_VALUE_SET blocks (Form extraction)
        if block_type == 'KEY_VALUE_SET':
            key, value = extract_key_value_pair(block, block_by_id)
            if key.strip().endswith(':'):
                key = key.rstrip(':')
                key = key.replace(':','')
            if key != '' or value != '':
                page_content[page_number]['KeyValuePairs'].append({key: value})
          
            
        # Handle LINE blocks (Text extraction)
        elif block_type == 'LINE':
            text_value = block.get('Text', '')
            # Only add if it doesn't already exist in key-value pairs or tables
            if not any(text_value in kv for kv in page_content[page_number]['KeyValuePairs']):
                page_content[page_number]['text'].append(text_value)

        # Handle TABLE blocks (Table extraction)
        elif block_type == 'TABLE':
            table_data = extract_table_data(block, block_by_id)
            ##print(f'table_data {len(table_data)}')
            # Avoid adding table content that is already in text or key-value pairs
            page_content[page_number]['tables'].append(table_data)
                    

    return page_content

def is_section_header(text, left_position, threshold=0.03):
    """Heuristic to detect section headers based on text and position"""
    return left_position < threshold 
    #or bool(re.match(r'^[A-Z].*:|^\d+(\.\d+)?\.', text))



def extract_key_value_pair(block, block_by_id):
    """Extract key-value pair from KEY_VALUE_SET block"""
    key = ""
    value = ""
    
       # Check if the block is a key block
    if 'KEY' in block['EntityTypes']:
        # Extract the key text
        if 'Relationships' in block:
            for rel in block['Relationships']:
                if rel['Type'] == 'CHILD':
                    for child_id in rel['Ids']:
                        key_block = block_by_id[child_id]
                        if key_block['BlockType'] == 'WORD':
                            key += key_block['Text'] + ' '

        # Extract the value text
        if 'Relationships' in block:
            for rel in block['Relationships']:
                if rel['Type'] == 'VALUE':
                    for value_id in rel['Ids']:
                        value_block = block_by_id[value_id]
                        if 'Relationships' in value_block:
                            for val_rel in value_block['Relationships']:
                                if val_rel['Type'] == 'CHILD':
                                    for child_id in val_rel['Ids']:
                                        word_block = block_by_id[child_id]
                                        if word_block['BlockType'] == 'WORD':
                                            value += word_block['Text'] + ' '

    return key, value


def extract_table_data(table_block, block_by_id):
    """Extract table data by traversing TABLE and CELL blocks"""
    table_data = {"Column Header": [], "Rows": []}
    
    relationships = table_block.get('Relationships', [])
    for relationship in relationships:
        if relationship.get('Type') == 'CHILD':
            child_ids = relationship.get('Ids', [])
            for child_id in child_ids:
                cell_block = block_by_id.get(child_id)
                if cell_block and cell_block.get('BlockType') == 'CELL':
                    cell_text = extract_text_from_cell(cell_block, block_by_id)
                    row_index = cell_block.get('RowIndex', 0)
                    col_index = cell_block.get('ColumnIndex', 0)
                    
                    if row_index == 1:
                        table_data["Column Header"].append(cell_text)
                    else:
                        if len(table_data["Rows"]) < row_index - 1:
                            table_data["Rows"].append([])
                        table_data["Rows"][row_index - 2].append(cell_text)

    return table_data


def extract_text_from_cell(cell_block, block_by_id):
    """Extract text from a CELL block in a table"""
    cell_text = []
    if 'Relationships' in cell_block:
        for rel in cell_block['Relationships']:
            if rel.get('Type') == 'CHILD':
                for grandchild_id in rel.get('Ids', []):
                    child_block = block_by_id.get(grandchild_id)
                    if child_block and child_block.get('BlockType') == 'WORD':
                        cell_text.append(child_block.get('Text', ''))
    return ' '.join(cell_text)


def build_output_string(output):
    """Builds a structured text string from the output."""
    output_string = []
    
    for page, content in output.items():
        output_string.append(f'"Page "{page}":"\n')
        
        for section in content['Sections']:
            left_position = section.get('LeftPosition', 0)  # Assuming you store LeftPosition in section
            
            table_count = len(section['Tables'])
            section_header = section['SectionHeader']
            key_value_count = len(section['KeyValuePairs'])
            print(f'table_count: {table_count}, key_value_count: {key_value_count}, section_header: {section_header}, section text: {len(section['Text'])}')
            if table_count != 0 or key_value_count !=0 or (section_header != '' and len(section['Text']) != 0):
                # Use formatting for section headers based on left position
                section_header_format = (
                    f"  **Section: {section['SectionHeader']}**\n"
                    if is_section_header(section['SectionHeader'], left_position)
                    else f"  Section: {section['SectionHeader']}\n"
                )
                output_string.append(section_header_format)
                output_string.append(f"  Text: {', '.join(section.get('Text', []))}\n")
                
                output_string.append(f"  Key-Value Pairs:\n")
                for kvp in section['KeyValuePairs']:
                    for key, value in kvp.items():
                        output_string.append(f"    {key}: {value}\n")
    
                output_string.append(f"  Tables:\n")
               
                for table_id, table_data in section['Tables'].items():
                    output_string.append(f"    {table_id}:\n")
                    output_string.append(f"      Column Header: {', '.join(table_data['Column Header'])}\n")
                    for index, row in enumerate(table_data['Rows'], start=1):
                        output_string.append(f"      Row{index}: {', '.join(row)}\n")
        output_string.append(f'"\n')
    return ''.join(output_string)

def build_output_string_withoutsection(output,coversheet_count):
    """Builds a structured text string from the output."""
    output_string = []
    pages = list(output.items())  # Convert to a list to know the length
    total_pages = len(pages)
    output_string.append(f'{{')
    for page, content in output.items():
        output_string.append(f'"Page {page-coversheet_count}":"\n')
        
        # Add the text content for the page
        if content.get('text'):
            content_text = [text.replace('\\','/').replace('"', '\\"') for text in content['text']]
            output_string.append(f"  Text: {', '.join(content_text)}\n")
        
        # Add the key-value pairs for the page
        if content.get('KeyValuePairs'):
            output_string.append(f"  Key-Value Pairs:\n")
            for kvp in content['KeyValuePairs']:
                for key, value in kvp.items():
                    content_key = key.replace('\\','/').replace('"','\\"')
                    content_value = value.replace('\\','/').replace('"','\\"')
                    output_string.append(f"    {content_key}: {content_value}\n")
        
        # Add the tables for the page
        if content.get('tables'):
            output_string.append(f"  Tables:\n")
            for table_index, table_data in enumerate(content['tables'], start=1):
                output_string.append(f"    Table {table_index}:\n")
                output_string.append(f"      Column Header: {', '.join(table_data['Column Header']).replace('\\','/').replace('"', '\\"')}\n")
                for row_index, row in enumerate(table_data['Rows'], start=1):
                    output_string.append(f"      Row{row_index}: {', '.join(row).replace('\\','/').replace('"', '\\"')}\n")
        
        
        if page == total_pages:
            output_string.append(f'"\n')
        else:
            output_string.append(f'",\n')
            
    output_string.append(f'}}')
    return ''.join(output_string)

def chunk_text_by_page(text, page_marker='"Page', char_limit=10000):
    chunks = []
    lines = text.splitlines()
    chunk = []
    
    for line in lines:
        if line.startswith(page_marker) and chunk:
            current_chunk = "\n".join(chunk)
            chunks.append(current_chunk)
            chunk = [line]
        else:
            chunk.append(line)
    if chunk:
        chunks.append("\n".join(chunk))
    
    # Separate chunks based on char_limit
    final_chunks = []
    temp_chunk = ""
    
    for chunk in chunks:
        if len(temp_chunk) + len(chunk) > char_limit:
            temp_chunk = temp_chunk.lstrip("{")
            temp_chunk = temp_chunk.rstrip(",}")
            temp_chunk = temp_chunk.replace('{"','"')
            final_chunks.append(f"{{{temp_chunk}}}")
            temp_chunk = chunk
            
        else:
           temp_chunk += "\n" + chunk
                
    if temp_chunk:
        temp_chunk = temp_chunk.rstrip(",")
        temp_chunk = temp_chunk.lstrip("{{")
        temp_chunk = temp_chunk.rstrip("}}")
        final_chunks.append(f"{{{temp_chunk}}}")
    
    return final_chunks
    

def build_segmented_data_simple_structure():
    bucket_name = 'qsrs-ocr-poc-dev'
    file_key = 'ocr-results/4928968_Redacted_clean_20241001-173934_6ad9b339c505ef409abc0b3e20f367c40426f5baf615f02205d47bd69a33276b.txt'
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    # Read the content of the object (file)
    content = response['Body'].read().decode('utf-8')
    
    clean_content = content.replace('{"text": {','').replace('}}','')
    # Parse the JSON content
    #json_data = json.loads(content)
    
    datachunking = os.getenv('datachunking')
    
    if datachunking == '1':
        chunks = chunk_text_by_page_simple(clean_content)
        for i, chunk in enumerate(chunks, 1):
            file_name = f'data-segments/4928968_Redacted_clean_chunks/4928968_Redacted_clean_chunk_{i}.txt'
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=chunk)
    

def chunk_text_by_page_simple(text, page_marker='"', char_limit=10000):
    
    chunks = []
    lines = text.splitlines()
    current_chunk = ""
    current_chunk_size = 0
    
    for line in lines:
        # Check if the line is a page marker, e.g., "1":", "2":", etc.
        if line.startswith(page_marker) and current_chunk:
            # Check if adding the new page exceeds the character limit
            if current_chunk_size + len(line) > char_limit:
                # Add the current chunk to the list and reset for the next chunk
                chunks.append(current_chunk)
                current_chunk = line
                current_chunk_size = len(line)
            else:
                current_chunk += "\n" + line
                current_chunk_size += len(line)
            print(f'current_chunk: {current_chunk}, current chunk size: {current_chunk_size}')    
        else:
            # Continue adding to the current chunk
            current_chunk += "\n" + line
            current_chunk_size += len(line)

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
    
def find_key_value_in_string(text, key):
    """Search for a key in the string and return the associated value."""
    # Compile a regex pattern to match the key followed by a colon and the associated value
    pattern = re.compile(rf"{key}\s*:\s*(\S+)")
    
    # Search the string for the key and associated value
    match = pattern.search(text)
    
    if match:
        return match.group(1)  # Return the first matching group (the value)
    
    return None  # If the key is not found
    
    
# Function to count instances of a text string across all pages
def count_text_across_pages(structured_output, target_text):
    total_count = 0
    
    for page_num, page_data in structured_output.items():
        if "text" in page_data:  # Ensure the page has a 'text' field
            total_count += page_data["text"].count(target_text)  # Count in each page's text
    
    return total_count