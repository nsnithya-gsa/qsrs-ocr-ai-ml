import os
import sys
import json
import boto3
import psycopg2
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = 'ai_human_dataset'
s3_bucket_name = 'test-results-to-database'

def lambda_handler(event, context):
    # initialize S3 client
    s3 = boto3.client('s3')

    connection = None
    cursor = None  # Initialize cursor here to avoid error in finally block if try block fails
    
    try:
        # Get bucket and file info from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Triggered by bucket: {bucket}, file: {key}")

        # Ensure the bucket matches the expected bucket name
        if bucket != s3_bucket_name:
            raise ValueError(f"Unexpected bucket name: {bucket}")
    
        # Download the JSON file from S3
        file_path = f"/tmp/{key.split('/')[-1]}"  # Save to the /tmp directory
        s3.download_file(bucket, key, file_path)
        logger.info(f"File downloaded successfully: {file_path}")
    
        # Read and parse the file
        with open(file_path, 'r') as file:
            data = json.load(file)
            logger.info(f"Loaded JSON data: {len(data)} records found")
    
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            host=os.getenv('ahrq-qsrs-rds-poc.cv4wcgcsavc4.us-east-1.rds.amazonaws.com'),
            port=os.getenv('5432'),
            database=os.getenv('postgres'),
            user=os.getenv('postgres'),
            password=os.getenv('$ICube2024')
        )
        cursor = connection.cursor()
        logger.info("Database connection established")

        all_fields = ["record_filenumber", "caseid", "modelid", "case_ai_retrieval_timestamp", "algorithmid", "questionid", 
        "llm_question", "llm_answer", "llm_reason", "human_abstraction_answer", "answer_comparison", "llm_result"]
    
        # Dynamically generate the SQL INSERT statement
        columns = ", ".join(all_fields)  # Join the field names into a comma-separated string
        placeholders = ", ".join(["%s"] * len(all_fields))  # Create placeholders for each field

        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # insert data into db
        for record in data:
            # Check if any field in `all_fields` is missing from the record
            missing_fields = [field for field in all_fields if field not in record]
            if missing_fields:
                logger.error(f"Record is missing required fields: {missing_fields}")
                continue  # Skip this record

            # Extract the values in the order of `all_fields`
            values = [record[field] for field in all_fields]
    
            # Execute the SQL INSERT statement
            cursor.execute(sql_insert, values)
    
        # Commit the transaction
        connection.commit()
        logger.info("Data successfully written to the database")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

    finally:
        # Clean up database connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        logger.info("Database connection closed")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data successfully ingested')
    }
