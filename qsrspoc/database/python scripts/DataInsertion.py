import json
import psycopg2
import os
from datetime import date

# Directory containing JSON files
folder_path = 'C:\\AHRQ Project\\JSON To PostgreSQL Data Insertion\\Base Line Data 6\\Data Set-JSON File Original'

# Get today's date in YYYY-MM-DD format
today_date = date.today().strftime('%Y-%m-%d')

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password=""
)
cur = conn.cursor()

# Fetch the max version_ai_snapshot_id from the table
cur.execute("SELECT COALESCE(MAX(version_ai_snapshot_id), 0) FROM t_ai_dataset")
max_version_id = cur.fetchone()[0]
new_version_id = max_version_id + 1  # Increment version_ai_snapshot_id or set to 1 if table is empty

# Get the current timestamp
# cur.execute("SELECT CURRENT_TIMESTAMP")
# current_timestamp = cur.fetchone()[0]
current_timestamp = date.today().strftime('%Y-%m-%d')

# Iterate through all JSON files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Ensure it's a JSON file
        file_path = os.path.join(folder_path, filename)

        # Extract record_filenumber from filename (before first underscore) - 4927782_Redacted_final_output.json
        # record_filenumber = filename.split('_')[0]
        record_filenumber = "_".join(filename.split('_')[:2])

        # Load JSON file
        with open(file_path) as file:
            data = json.load(file)

        # Insert data into PostgreSQL table
        for algorithm_id, question_dict in data.items():
            # Check if algorithm_id is one of the special cases and modify accordingly
            if algorithm_id.startswith("OOOI"):
                standardized_algorithm_id = "OOOI"
            elif algorithm_id.startswith("Medication"):
                standardized_algorithm_id = "Medication"
            else:
                standardized_algorithm_id = algorithm_id  # Leave others unchanged

            for question_id, fields in question_dict.items():
                # Handle empty values
                question = fields.get('Question') or None
                answer = fields.get('Answer') or None
                reason = fields.get('Reason') or None
                pages_used = fields.get('Pages used')
                pages_used = None if not pages_used else ','.join(map(str, pages_used))
                confidence_score = fields.get('Confidence score') or None

                cur.execute(
                    """
                    INSERT INTO t_ai_dataset (record_filenumber, case_id, model_id, case_ai_retrieval_timestamp, algorithm_id, question_id, llm_question, llm_answer, llm_reason, pages_used, confidence_score, version_ai_snapshot_id, snapshot_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (record_filenumber+".pdf", None, 2, today_date, standardized_algorithm_id, question_id, question, answer,
                     reason, pages_used, confidence_score, new_version_id, current_timestamp)
                )

# Commit changes and close connection
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()