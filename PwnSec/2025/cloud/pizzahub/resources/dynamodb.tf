resource "aws_dynamodb_table" "receipts" {
  name           = "pizza_orders_receipts"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }

  tags = {
    app = "pizza"
  }
}

resource "aws_dynamodb_table" "secrets" {
  name           = "pizza_secrets"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "secret_id"

  attribute {
    name = "secret_id"
    type = "S"
  }

  tags = {
    app = "pizza-secrets"
  }
}

resource "aws_dynamodb_table_item" "FLAG" {
  table_name = aws_dynamodb_table.secrets.name
  hash_key   = "secret_id"

  item = jsonencode({
    secret_id = { S = "1" }
    name      = { S = "SECRET_RECEIPT" }
    value     = { S = "flag{WIxFGEGtIt5KXqACJnK7CmuBq6ygQ05Xd6EROQxhLr9CKH363WJ3J5QadKg}" }
  })
}

