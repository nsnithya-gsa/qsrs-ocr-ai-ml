# Configuring Terraform to use S3 as a backend for storing the state file.
# TODO: Enable versioning in the backend bucket
# TODO: Specify versions for the AWS providers
# TODO: Create the bucket if it doesn't exist 

/*-------------------------------
terraform {
  backend "s3" {
    bucket = "ahrq-terraform-ocr" # pass as parameter
    key    = "terraform.tfstate" # pass as parameter
	region = "us-east-1" # pass as parameter

  }
}

--------------------------------*/

# Define the provider and AWS credentials
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

########################################
# S3 Bucket CREATION
###################################

resource "aws_s3_bucket" "my_bucket" {
  bucket   = var.bucket_name
  acl    = "private"
  tags = {
   Name        = var.bucket_name
   Environment = "Dev"
  }
}

resource "aws_s3_bucket" "my_bucket1" {
  bucket   = var.bucket_name1
  acl    = "private"
  tags = {
   Name        = var.bucket_name1
   Environment = "Dev"
  }
}


###################################
# CREATING SUB FOLDERS UNDER S3 Buckets
###################################

resource "aws_s3_bucket_object" "landing" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "landing/"  
}

resource "aws_s3_bucket_object" "processed" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "processed/"  
}
resource "aws_s3_bucket_object" "ocr-results" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ocr-results/"  
}
resource "aws_s3_bucket_object" "ai-ml" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ai-ml/"  
}
resource "aws_s3_bucket_object" "config" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "config/"  
}
resource "aws_s3_bucket_object" "cleaned-data" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "cleaned-data/"  
}
resource "aws_s3_bucket_object" "structured-data" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "structured-data/"  
}
resource "aws_s3_bucket_object" "data-segments" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "data-segments/"  
}
resource "aws_s3_bucket_object" "folder9" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "logs/"  
}

resource "aws_s3_bucket_object" "ocr-pdf-preprocess" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ocr-pdf-preprocess/"  
}

resource "aws_s3_bucket_object" "ocr-pdf-split-results" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ocr-pdf-split-results/"  
}

resource "aws_s3_bucket_object" "question-embedding-input" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "question-embedding-input/"  
}

resource "aws_s3_bucket_object" "question-embedding-output" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "question-embedding-output/"  
}


###################################
# CREATING FOLDERS UNDER SUB FOLDERS
###################################

resource "aws_s3_bucket_object" "code" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ai-ml/code/"  
}

resource "aws_s3_bucket_object" "biobert-model" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ai-ml/biobert-model/"  
}
resource "aws_s3_bucket_object" "llm-output" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ai-ml/llm-output/"  
}
resource "aws_s3_bucket_object" "page-embeddings" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ai-ml/page-embeddings/"  
}

resource "aws_s3_bucket_object" "deploy" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ai-ml/deploy/"  
}

resource "aws_s3_bucket_object" "passed-step-function-data" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "ai-ml/passed-step-function-data/"  
}

resource "aws_s3_bucket_object" "ocr" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "config/ocr/"  
}

resource "aws_s3_bucket_object" "folder10" {
  bucket = aws_s3_bucket.my_bucket.bucket
  key    = "config/ai-ml/"  
}

##################################################################
#    SQS MODULE
##################################################################
/*------------
module "sqs_module" {
  source = "./modules/sqs"
  sqs_queue_name                  = var.sqs_queue_name
  sqs_delay_seconds               = var.sqs_delay_seconds
  sqs_max_message_size            = var.sqs_max_message_size
  sqs_message_retention_seconds   = var.sqs_message_retention_seconds
  sqs_receive_wait_time_seconds   = var.sqs_receive_wait_time_seconds
  sqs_visibility_timeout_seconds  = var.sqs_visibility_timeout_seconds
}
--------*/
##################################################################
#    SNS MODULE
##################################################################
module "sns" {
  for_each = var.topic_to_queues
  source   = "./modules/sns"
  topic_name       = each.key
  sqs_queue_names  = { for q in each.value : q => {} }
}

##################################################################
#    BEGIN AWS BATCH MODULE
##################################################################

#############################
# IAM Role: EC2 instance role for ECS
#############################

resource "aws_iam_role" "ecs_instance_role" {
  name = "ecsInstanceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_instance_policy" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecsInstanceProfile"
  role = aws_iam_role.ecs_instance_role.name
}

#############################
# IAM Role: AWS Batch Service Role
#############################

resource "aws_iam_role" "batch_service_role" {
  name = "aws-batch-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "batch.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "batch_service_role_policy" {
  role       = aws_iam_role.batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

#############################
# AWS Batch Compute Environment (EC2)
#############################

resource "aws_batch_compute_environment" "ec2_compute_env" {
  compute_environment_name = "batch-ec2-compute-env"
  type                     = "MANAGED"
  service_role             = aws_iam_role.batch_service_role.arn

  compute_resources {
    type              = "EC2"
    allocation_strategy = "BEST_FIT"
    instance_role     = aws_iam_instance_profile.ecs_instance_profile.arn
    instance_type    = ["inf1.2xlarge"]
    min_vcpus         = 0
    max_vcpus         = 4
    desired_vcpus     = 0
    subnets           = ["subnet-02730b985e1160a2a"] # Replace subnet-id with actual subnet-id
    security_group_ids = ["sg-09403737e61b5c2e8"] # Replace security-group-id-id with actual security-group-id
  }
}

#############################
# AWS Batch Job Queue
#############################

resource "aws_batch_job_queue" "job_queue" {
  name                 = var.aws_batch
  state                = "ENABLED"
  priority             = 1
  compute_environments = [aws_batch_compute_environment.ec2_compute_env.arn]
}

#############################
# AWS Batch Job Definition
#############################

resource "aws_batch_job_definition" "qsrs_ocr_aiml_job" {
  name = var.aws_batch_def
  type = "container"

  container_properties = jsonencode({
    image: "amazonlinux",
    vcpus: 1,
    memory: 512,
    command: ["echo", "Hello from EC2 AWS Batch!"]
  })
}


##################################################################
#    ECR REPO
##################################################################
resource "aws_ecr_repository" "repo" {
  name = var.repo_name
  image_tag_mutability = "MUTABLE"

  # Uncomment the below to enable repo scanning 
  image_scanning_configuration {
     scan_on_push = true
  }
}

##################################################################
#    BEGIN SageMaker Provisioning
##################################################################

############################
# IAM Role for SageMaker
############################
resource "aws_iam_role" "sagemaker_execution_role" {
  name = "sagemaker-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "sagemaker.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_basic_permissions" {
  role       = aws_iam_role.sagemaker_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

# Attach full access to S3
resource "aws_iam_role_policy" "s3_full_access_policy" {
  name = "S3FullAccessForSageMaker"
  role = aws_iam_role.sagemaker_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:*"
        ],
        Resource = "*"
      }
    ]
  })
}

############################
# SageMaker Model
############################
resource "aws_sagemaker_model" "model" {
  name	= var.sagemaker_model
  execution_role_arn = aws_iam_role.sagemaker_execution_role.arn

  primary_container {
    image           = "763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:1.10.2-transformers4.17.0-cpu-py38-ubuntu20.04"  # Change to your preferred image
    model_data_url  = "s3://ahrq-qsrs-ml-poc/deploy/model.tar.gz"             # Replace with your S3 path
    mode            = "SingleModel"
  }
}

############################
# SageMaker Endpoint Configuration
############################
resource "aws_sagemaker_endpoint_configuration" "endpoint_config" {
  name = var. sagemaker_endpoint_config

  production_variants {
    variant_name           = "AllTraffic"
    model_name             = aws_sagemaker_model.model.name
    initial_instance_count = 1
    instance_type          = "ml.m4.xlarge"  # Replace instance_type
  }
}

############################
# SageMaker Endpoint
############################
resource "aws_sagemaker_endpoint" "endpoint" {
  name                 = var.sagemaker_endpoint
  endpoint_config_name = aws_sagemaker_endpoint_configuration.endpoint_config.name
}
