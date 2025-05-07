CREATE TRIGGER t_human_primary_dataset_trigger
AFTER INSERT OR UPDATE OR DELETE ON t_human_primary_dataset
FOR EACH ROW EXECUTE FUNCTION audit_t_human_primary_dataset();