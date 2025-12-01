output "blvkrose_access_key_id" {
  value     = aws_iam_access_key.blvk_keys.id
  sensitive = false
}
output "blvkrose_secret_access_key" {
  value     = aws_iam_access_key.blvk_keys.secret
  sensitive = true
}

output "sqs_queue_url" {
  value = aws_sqs_queue.orders.id
}

output "lambda_function_name" {
  value = aws_lambda_function.order_processor.function_name
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.receipts.name
}
