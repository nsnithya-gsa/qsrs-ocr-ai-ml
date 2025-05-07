CREATE OR REPLACE FUNCTION audit_t_ai_dataset()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO t_ai_dataset_audit (record_filenumber, case_id,	model_id, case_ai_retrieval_timestamp, algorithm_id, question_id, llm_question,	llm_answer,	llm_reason, pages_used, confidence_score, operation_type, user_name, version_ai_snapshot_id, snapshot_date)
        VALUES (NEW.record_filenumber, NEW.case_id,	NEW.model_id, NEW.case_ai_retrieval_timestamp, NEW.algorithm_id, NEW.question_id, NEW.llm_question,	NEW.llm_answer,	NEW.llm_reason, NEW.pages_used, NEW.confidence_score, 'INSERT', current_user, NEW.version_ai_snapshot_id, NEW.snapshot_date);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO t_ai_dataset_audit (record_filenumber, case_id,	model_id, case_ai_retrieval_timestamp, algorithm_id, question_id, llm_question,	llm_answer,	llm_reason, pages_used, confidence_score, operation_type, user_name, version_ai_snapshot_id, snapshot_date)
        VALUES (NEW.record_filenumber, NEW.case_id,	NEW.model_id, NEW.case_ai_retrieval_timestamp, NEW.algorithm_id, NEW.question_id, NEW.llm_question,	NEW.llm_answer,	NEW.llm_reason, NEW.pages_used, NEW.confidence_score, 'UPDATE', current_user, NEW.version_ai_snapshot_id, NEW.snapshot_date);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO t_ai_dataset_audit (record_filenumber, case_id,	model_id, case_ai_retrieval_timestamp, algorithm_id, question_id, llm_question,	llm_answer,	llm_reason, pages_used, confidence_score, operation_type, user_name, version_ai_snapshot_id, snapshot_date)
        VALUES (OLD.record_filenumber, OLD.case_id,	OLD.model_id, OLD.case_ai_retrieval_timestamp, OLD.algorithm_id, OLD.question_id, OLD.llm_question,	OLD.llm_answer,	OLD.llm_reason, OLD.pages_used, OLD.confidence_score, 'DELETE', current_user, OLD.version_ai_snapshot_id, OLD.snapshot_date);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;