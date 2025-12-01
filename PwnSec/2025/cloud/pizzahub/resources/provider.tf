terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region                      = var.region
  access_key                  = var.access_key
  secret_key                  = var.secret_key
  skip_credentials_validation = true
  skip_metadata_api_check     = true

  endpoints {
    sqs         = "${var.localstack_endpoint}"
    lambda      = "${var.localstack_endpoint}"
    dynamodb    = "${var.localstack_endpoint}"
    iam         = "${var.localstack_endpoint}"
    sts         = "${var.localstack_endpoint}"
    cloudwatch  = "${var.localstack_endpoint}"
  }
}
