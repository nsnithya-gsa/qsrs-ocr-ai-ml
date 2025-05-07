CREATE TRIGGER t_ai_dataset_trigger
AFTER INSERT OR UPDATE OR DELETE ON t_ai_dataset
FOR EACH ROW EXECUTE FUNCTION audit_t_ai_dataset();