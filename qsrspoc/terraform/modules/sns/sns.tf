resource "aws_sns_topic" "this" {
  name = var.topic_name
}

# Create DLQs
resource "aws_sqs_queue" "dlqs" {
  for_each = var.sqs_queue_names

  name = "${each.key}-dlq"
}

# Create main queues with DLQ redrive policy
resource "aws_sqs_queue" "queues" {
  for_each = var.sqs_queue_names

  name = each.key

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlqs[each.key].arn
    maxReceiveCount     = 5
  })
}

# Allow SNS to send to SQS
resource "aws_sqs_queue_policy" "queue_policy" {
  for_each = aws_sqs_queue.queues

  queue_url = each.value.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowSNS"
      Effect    = "Allow"
      Principal = "*"
      Action    = "sqs:SendMessage"
      Resource  = each.value.arn
      Condition = {
        ArnEquals = {
          "aws:SourceArn" = aws_sns_topic.this.arn
        }
      }
    }]
  })
}

# Subscribe queues to topic
resource "aws_sns_topic_subscription" "subs" {
  for_each = aws_sqs_queue.queues

  topic_arn = aws_sns_topic.this.arn
  protocol  = "sqs"
  endpoint  = each.value.arn
}