# Define the variables
variable "aws_region" {
  description = "The AWS region where the S3 bucket will be created"
  default     = "us-east-1"
}

variable "aws_access_key" {
  description = "Your AWS access key"
}

variable "aws_secret_key" {
  description = "Your AWS secret key"
}

variable "bucket_name" {
  description = "The name of the S3 bucket"
}

variable "bucket_name1" {
  description = "The name of the pdf drop location S3 bucket"
}

variable "aws_batch" {
  description = "The name of the AWS Batch used in this account"
}

variable "aws_batch_def" {
  description = "The name of the AWS Batch Definition used in this account"
}


variable "repo_name" {
  description = "The name of ECR Repository for the images to be pushed"
}

variable "sagemaker_model" {
  description = "The name of Sage Maker Model"
}

variable "sagemaker_endpoint" {
  description = "The name of Sage Maker Endpoint"
}

variable "sagemaker_endpoint_config" {
  description = "The name of Sage Maker Endpoint Configuration"
}

variable "versioning_bucket_name" {
  description = "The name of the versioning S3 bucket "
}

# SQS
variable sqs_queue_name {
  description = "The name of the SQS Queue"
  default = "qsrs-ocr-dev-queue"
}

variable sqs_delay_seconds {
  description = "SQS Delay Seconds"
  default = 60

}
variable sqs_max_message_size {
  description = "SQS Max Message Size"
  default = 15000
}
variable sqs_message_retention_seconds {
  description = "SQS Message Retention Seconds"
  default = 600
}
variable sqs_receive_wait_time_seconds {
  description = "Receive Wait Time Seconds"
  default = 10
}
variable sqs_visibility_timeout_seconds {
  description = "Visibility Timeout Seconds"
  default = 30
}

# SNS
variable "topic_to_queues" {
  description = "Map of SNS topic name to list of SQS queue names"
  type        = map(list(string))
}



# VPC
variable "aws_vpc_id" {
  description = "The VPC Id"
  default = "vpc-08bf02cf3769d9aea"
}


