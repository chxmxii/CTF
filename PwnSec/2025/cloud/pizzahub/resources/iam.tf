data "aws_iam_policy_document" "lambda_assume" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "pizza-lambda-exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:GetItem"
    ]
    resources = [
      aws_dynamodb_table.receipts.arn
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Scan"
    ]
    resources = [
      aws_dynamodb_table.secrets.arn
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:ListTables"
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
  
  statement {
    effect = "Allow"
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]
    resources = [
      aws_sqs_queue.orders.arn
    ]
  }
}

resource "aws_iam_role_policy" "lambda_exec_policy" {
  name   = "pizza-lambda-policy"
  role   = aws_iam_role.lambda_exec.id
  policy = data.aws_iam_policy_document.lambda_policy.json
}


resource "aws_iam_user" "blvkrose" {
  name = "blvkrose"
  path = "/users/"
}

data "aws_iam_policy_document" "blvk_policy" {
  statement {
    sid    = "AllowCreateNamedLambda"
    effect = "Allow"
    actions = [
      "lambda:CreateFunction",
      "lambda:UpdateFunctionCode",
      "lambda:DeleteFunction",
      "lambda:InvokeFunction"
    ]
    resources = [
      "arn:aws:lambda:${var.region}:000000000000:function:blvkrose-*"
    ]
  }

  statement {
    sid      = "AllowPassRole"
    effect   = "Allow"
    actions  = ["iam:PassRole"]
    resources = [aws_iam_role.lambda_exec.arn]
  }

  statement {
    sid    = "AllowListLambda"
    effect = "Allow"
    actions = [
      "lambda:ListFunctions",
      "lambda:GetFunction"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "AllowSQS"
    effect = "Allow"
    actions = [
      "sqs:SendMessage",
      "sqs:GetQueueUrl",
      "sqs:ListQueues"
    ]
    resources = [aws_sqs_queue.orders.arn]
  }

  statement {
    sid    = "AllowReadPizzaReceipts"
    effect = "Allow"
    actions = [
      "dynamodb:GetItem",
      "dynamodb:Query",
      "dynamodb:Scan"
    ]
    resources = [
      "arn:aws:dynamodb:${var.region}:000000000000:table/pizza_orders_receipts"
    ]
  }

  statement {
    sid    = "AllowReadOwnPolicies"
    effect = "Allow"
    actions = [
      "iam:GetUser",
      "iam:ListAttachedUserPolicies",
      "iam:ListUserPolicies",
      "iam:GetUserPolicy"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${aws_iam_user.blvkrose.name}"
    ]
  }
}

resource "aws_iam_user_policy" "blvk_policy" {
  name   = "blvkrose-user-policy"
  user   = aws_iam_user.blvkrose.name
  policy = data.aws_iam_policy_document.blvk_policy.json
}

resource "aws_iam_access_key" "blvk_keys" {
  user = aws_iam_user.blvkrose.name
}

data "aws_caller_identity" "current" {}
