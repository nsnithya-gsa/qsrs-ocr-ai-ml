output "sns_topic_arns" {
  value = {
    for topic, mod in module.sns :
    topic => mod.topic_arn
  }
}

output "sqs_queue_arns" {
  value = {
    for topic, mod in module.sns :
    topic => mod.queue_arns
  }
}

output "dlq_arns" {
  value = {
    for topic, mod in module.sns :
    topic => mod.dlq_arns
  }
}
