CREATE TABLE t_ai_dataset_audit 
(
	audit_id BIGSERIAL PRIMARY KEY,
	operation_type VARCHAR(10) CHECK (operation_type IN ('INSERT', 'UPDATE', 'DELETE')),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_name VARCHAR(50),	
	record_filenumber VARCHAR(25),
	case_id VARCHAR(25),	
	model_id INTEGER,
	case_ai_retrieval_timestamp TIMESTAMP,	
	algorithm_id VARCHAR(50),
	question_id VARCHAR(100),
	llm_question VARCHAR,	
	llm_answer VARCHAR,	
	llm_reason VARCHAR,
	pages_used VARCHAR,
	confidence_score NUMERIC(32, 16),
	version_ai_snapshot_id INT,
	snapshot_date TIMESTAMP
);

ALTER TABLE t_ai_dataset_audit
ADD CONSTRAINT t_ai_dataset_audit_fkey
FOREIGN KEY (version_ai_snapshot_id, record_filenumber, case_ai_retrieval_timestamp, algorithm_id, question_id)
REFERENCES t_ai_dataset(version_ai_snapshot_id, record_filenumber, case_ai_retrieval_timestamp, algorithm_id, question_id);