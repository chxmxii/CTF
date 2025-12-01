variable "region" {
  type    = string
  default = "eu-west-1"
}

variable "localstack_endpoint" {
  type    = string
  default = "http://localstack:4566"
}

variable "lambda_runtime" {
  type    = string
  default = "python3.8"
}

variable "lambda_handler" {
  type    = string
  default = "lambda_function.lambda_handler"
}

variable "lambda_function_name" {
  type    = string
  default = "orders-processor-lambda"
}

variable "access_key" { 
  type = string 
}

variable "secret_key" { 
  type = string
}
