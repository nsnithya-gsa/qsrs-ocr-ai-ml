variable "topic_name" {
  type = string
}

variable "sqs_queue_names" {
  description = "Map of queue name => config (empty object)"
  type        = map(any)
  default     = {}
}
