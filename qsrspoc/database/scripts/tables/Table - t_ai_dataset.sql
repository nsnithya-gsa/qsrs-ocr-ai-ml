CREATE TABLE t_ai_dataset
(
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
	snapshot_date TIMESTAMP,
	primary key(version_ai_snapshot_id, record_filenumber, case_ai_retrieval_timestamp, algorithm_id, question_id)
);

ALTER TABLE t_ai_dataset
ADD CONSTRAINT fk_model_id
FOREIGN KEY (model_id)
REFERENCES t_ai_model(model_id);