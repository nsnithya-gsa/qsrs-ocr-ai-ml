CREATE TABLE t_human_primary_dataset
(
	record_filenumber VARCHAR(25),
	case_id VARCHAR(25),	
	algorithm_id VARCHAR(50),
	question_id VARCHAR(100),
	human_abstraction_answer VARCHAR,
	primary key(record_filenumber,algorithm_id,question_id)
);