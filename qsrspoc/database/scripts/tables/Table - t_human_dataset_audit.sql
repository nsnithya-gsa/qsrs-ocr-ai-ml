CREATE TABLE t_human_dataset_audit 
(
    audit_id BIGSERIAL PRIMARY KEY,
    operation_type VARCHAR(10) CHECK (operation_type IN ('INSERT', 'UPDATE', 'DELETE')),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	user_name VARCHAR(50),
    record_filenumber VARCHAR(25),
	case_id VARCHAR(25),
    algorithm_id VARCHAR(50),
    question_id VARCHAR(100),
    human_abstraction_answer VARCHAR,
	version_human_id_snapshot INT,
	snapshot_date TIMESTAMP
);

ALTER TABLE t_human_dataset_audit
ADD CONSTRAINT t_human_dataset_audit_fkey
FOREIGN KEY (version_human_snapshot_id, record_filenumber,algorithm_id,question_id)
REFERENCES t_human_dataset(version_human_snapshot_id, record_filenumber,algorithm_id,question_id);