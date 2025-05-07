aws_access_key = ""
aws_secret_key = ""
bucket_name    = "qsrs-ocr-poc-dev1"
bucket_name1   = "qsrs-ocr-poc-pdf-drop-location-dev1"
repo_name	   = "qsrs-ocr-awsbatch-pe1-repo"
versioning_bucket_name = "qsrs-ocr-poc-dev1"
sagemaker_model = "biobert-model-custom-v6"
sagemaker_endpoint = "biobert-model-endpoint-custom-v6"
sagemaker_endpoint_config = "biobert-model-endpoint-custom-v6-config"
aws_batch	=	"qsrs-ocr-env-pe1-ec2-awsbatch"
aws_batch_def	=	"batch-ec2-job-def"

topic_to_queues = {
  "ocr-process-completion-notification-1" = ["ocr-process-completion-queue-1"],
  "textract-jobcompletion-notification-1" = ["textract-jobcompletion-queue-1"]
}