locals {
  tags-index = "tags-index"
}

# DynamoDB Table for image metadata
resource "aws_dynamodb_table" "image_table" {
  name         = "Image"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "userId"
  range_key = "imageId"

  attribute {
    name = "userId"
    type = "S"
  }

  attribute {
    name = "imageId"
    type = "S"
  }

  attribute {
    name = "tags"
    type = "S"
  }

  # GSI on tags
  global_secondary_index {
    name            = local.tags-index
    hash_key        = "tags"
    projection_type = "ALL"

  }
}