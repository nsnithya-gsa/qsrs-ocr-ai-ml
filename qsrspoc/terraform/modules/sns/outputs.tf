output "topic_arn" {
  value = aws_sns_topic.this.arn
}

output "queue_arns" {
  value = { for k, v in aws_sqs_queue.queues : k => v.arn }
}

output "dlq_arns" {
  value = { for k, v in aws_sqs_queue.dlqs : k => v.arn }
}

