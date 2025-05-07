CREATE OR REPLACE FUNCTION audit_t_human_primary_dataset()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO t_human_primary_dataset_audit (record_filenumber, case_id, algorithm_id, question_id, human_abstraction_answer, operation_type, user_name)
        VALUES (NEW.record_filenumber, NEW.case_id, NEW.algorithm_id, NEW.question_id, NEW.human_abstraction_answer, 'INSERT', current_user);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO t_human_primary_dataset_audit (record_filenumber, case_id, algorithm_id, question_id, human_abstraction_answer, operation_type, user_name)
        VALUES (NEW.record_filenumber, NEW.case_id, NEW.algorithm_id, NEW.question_id, NEW.human_abstraction_answer, 'UPDATE', current_user);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO t_human_primary_dataset_audit (record_filenumber, case_id, algorithm_id, question_id, human_abstraction_answer, operation_type, user_name)
        VALUES (OLD.record_filenumber, OLD.case_id, OLD.algorithm_id, OLD.question_id, OLD.human_abstraction_answer, 'DELETE', current_user);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;