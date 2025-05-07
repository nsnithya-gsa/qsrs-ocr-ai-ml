import psycopg2
import json
import re
from datetime import datetime

# Load the JSON file
with open('C:\\AHRQ Project\\JSON To PostgreSQL Data Insertion\\Data\\process_log_032025.json') as file:
    data = json.load(file)

# Connect to your PostgreSQL DB
conn = psycopg2.connect(
    host="",
    database="",
    user="",
    password=""
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Retrieve the latest execution_datetime from the database
cur.execute("SELECT COALESCE(MAX(execution_datetime), '1900-01-01') FROM t_process_algorithm_status")
latest_execution_datetime = cur.fetchone()[0]
print(f"Latest execution datetime : {latest_execution_datetime}")

# Track duplicates and processed records
duplicate_entries = []
processed_entries = []

# Insert only new records into the table
for entry in data:
    bucket_name = entry.get('bucketname', '')
    file_path = entry.get('filepath', '')

    # Extract record_filenumber using regex pattern
    # pattern = r"\/([^\/]+?)(?:_|\.)"
    pattern = r"\/([^\/]+)(?:_embeddings\.json|_structured\.txt|_cleaned\.json|\.pdf)$"
    match = re.search(pattern, file_path)
    record_filenumber = match.group(1) if match else None
    record_filenumber = record_filenumber+".pdf"

    execution_datetime = entry.get('datetime', '')
    file_size = entry.get('filesize', '')

    # Process page count
    page_count = entry.get('pagecount', '')
    if isinstance(page_count, int):
        page_count = page_count
    elif isinstance(page_count, str) and page_count.isdigit():
        page_count = int(page_count)
    else:
        page_count = None  # Use None to insert NULL into the DB

    status = entry.get('status', '')
    message = entry.get('message', '')
    # Process num_questions
    num_question = entry.get("num_questions", None)  # Default to None if missing

    # Only process records with execution_datetime > latest_execution_datetime
    if execution_datetime > str(latest_execution_datetime):
        try:
            cur.execute("""
                INSERT INTO t_process_algorithm_status (record_filenumber, file_date, bucket_name, file_path, execution_datetime, file_size, page_count, status, message, num_question)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (record_filenumber, message, execution_datetime) DO NOTHING
                RETURNING record_filenumber;
            """, (record_filenumber, None, bucket_name, file_path, execution_datetime, file_size, page_count, status, message, num_question))

            # Fetch result, if none returned, it was a duplicate
            result = cur.fetchone()
            if result is None:
                duplicate_entries.append((record_filenumber, message, execution_datetime))
            else:
                processed_entries.append((record_filenumber, execution_datetime))

        except Exception as e:
            print(f"Error inserting record: {record_filenumber}, {message}, {execution_datetime} - {e}")

# Commit the transaction
conn.commit()

# Write an SQL query to fetch data from a table
queryRead = "select record_filenumber, message, execution_datetime from t_process_algorithm_status where file_date is null order by record_filenumber, execution_datetime"

# Execute the query
cur.execute(queryRead)

# Fetch all rows from the executed query
rows = cur.fetchall()

# Process and print the rows
constant_record_filenumber = 0
fdate = None
for row in rows:
    record_filenumberCol0 = row[0]
    messageCol1 = row[1]
    execution_datetimeCol2 = row[2]
    if messageCol1 == "OCR process started": # For Valid condition
        fdate = datetime.strptime(execution_datetimeCol2.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        constant_record_filenumber = record_filenumberCol0
    elif fdate: # For Invalid condition - File Started with message Other than - OCR process started
        if (fdate.date() != execution_datetimeCol2.date()) or (constant_record_filenumber != record_filenumberCol0):
            fdate = None

    update_query = """
            UPDATE t_process_algorithm_status
            SET file_date = %s 
            WHERE file_date is null  
            AND record_filenumber = %s 
            AND message=%s 
            AND execution_datetime = %s;
        """
    cur.execute(update_query, (fdate, record_filenumberCol0,messageCol1,execution_datetimeCol2))

conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

# Print summary
print("\nProcessing completed.")
print(f"{len(processed_entries)} new records inserted.")
if duplicate_entries:
    print(f"{len(duplicate_entries)} duplicates ignored:")
    for dup in duplicate_entries:
        print(f"Record_filenumber: {dup[0]}, Message: {dup[1]}, Execution_datetime: {dup[2]}")
