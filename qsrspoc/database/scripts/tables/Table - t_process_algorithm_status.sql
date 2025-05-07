CREATE TABLE t_process_algorithm_status
(
    record_filenumber VARCHAR(25),
    message VARCHAR(100),
    status VARCHAR(10),
    execution_datetime TIMESTAMP,
    file_date TIMESTAMP,
    bucket_name VARCHAR(255),
    file_path VARCHAR(255),
    file_size INTEGER,
    page_count INTEGER,
    num_question INTEGER,
    primary key(record_filenumber, message, execution_datetime)
);