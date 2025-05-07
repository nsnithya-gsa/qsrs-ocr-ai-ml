CREATE TABLE t_human_dataset
(
	record_filenumber VARCHAR(25),
	case_id VARCHAR(25),	
	algorithm_id VARCHAR(50),
	question_id VARCHAR(100),
	human_abstraction_answer VARCHAR,
	version_human_snapshot_id INT,
	snapshot_date TIMESTAMP,
	primary key(version_human_snapshot_id, record_filenumber,algorithm_id,question_id)
);