resource "aws_lambda_function" "order_processor" {
  function_name    = "blvk-order-processor"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  publish          = true
  role             = aws_iam_role.lambda_exec.arn

  filename         = "${path.module}/lambda/lambda_function.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/lambda_function.zip")
  
  environment {
    variables = {
      RECEIPTS_TABLE = aws_dynamodb_table.receipts.name
      REGION         = var.region
    }
  }
}
