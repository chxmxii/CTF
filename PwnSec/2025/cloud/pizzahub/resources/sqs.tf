resource "aws_sqs_queue" "orders" {
  name                      = "pizza-orders"
  visibility_timeout_seconds = 30
  message_retention_seconds  = 1200
}

resource "aws_sqs_queue_policy" "orders_policy" {
  queue_url = aws_sqs_queue.orders.id
  policy    = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          AWS = "arn:aws:iam::000000000000:user/blvkrose"
        }
        Action   = "sqs:SendMessage"
        Resource = aws_sqs_queue.orders.arn
      }
    ]
  })
}

resource "aws_lambda_event_source_mapping" "sqs_to_lambda" {
  event_source_arn = aws_sqs_queue.orders.arn
  function_name    = aws_lambda_function.order_processor.arn
  enabled          = true
  batch_size       = 1
}
