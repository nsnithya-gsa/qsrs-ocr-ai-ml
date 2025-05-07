CREATE TABLE t_human_primary_dataset_audit 
(
    audit_id BIGSERIAL PRIMARY KEY,
    operation_type VARCHAR(10) CHECK (operation_type IN ('INSERT', 'UPDATE', 'DELETE')),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_name VARCHAR(50),
    record_filenumber VARCHAR(25),
	case_id VARCHAR(25),
    algorithm_id VARCHAR(50),
    question_id VARCHAR(100),
    human_abstraction_answer VARCHAR
);

ALTER TABLE t_human_primary_dataset_audit
ADD CONSTRAINT t_human_primary_dataset_audit_fkey
FOREIGN KEY (record_filenumber,algorithm_id,question_id)
REFERENCES t_human_primary_dataset(record_filenumber,algorithm_id,question_id);