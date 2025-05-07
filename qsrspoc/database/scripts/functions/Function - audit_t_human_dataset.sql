CREATE OR REPLACE FUNCTION audit_t_human_dataset()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO t_human_dataset_audit (record_filenumber, case_id, algorithm_id, question_id, human_abstraction_answer, operation_type, user_name, version_human_snapshot_id, snapshot_date)
        VALUES (NEW.record_filenumber, NEW.case_id, NEW.algorithm_id, NEW.question_id, NEW.human_abstraction_answer, 'INSERT', current_user, NEW.version_human_snapshot_id, NEW.snapshot_date);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO t_human_dataset_audit (record_filenumber, case_id, algorithm_id, question_id, human_abstraction_answer, operation_type, user_name, version_human_snapshot_id, snapshot_date)
        VALUES (NEW.record_filenumber, NEW.case_id, NEW.algorithm_id, NEW.question_id, NEW.human_abstraction_answer, 'UPDATE', current_user, NEW.version_human_snapshot_id, NEW.snapshot_date);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO t_human_dataset_audit (record_filenumber, case_id, algorithm_id, question_id, human_abstraction_answer, operation_type, user_name, version_human_snapshot_id, snapshot_date)
        VALUES (OLD.record_filenumber, OLD.case_id, OLD.algorithm_id, OLD.question_id, OLD.human_abstraction_answer, 'DELETE', current_user, OLD.version_human_snapshot_id, OLD.snapshot_date);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;