# Lambda IAM role with necessary permissions
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Separate IAM policy for S3 and DynamoDB access
resource "aws_iam_policy" "lambda_dynamodb_s3_policy" {
  name        = "lambda-dynamodb-s3-policy"
  description = "Policy for Lambda function to access S3 and DynamoDB"

  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        Resource = [
          "${aws_s3_bucket.image_bucket.arn}",
          "${aws_s3_bucket.image_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:GetItem",
          # "dynamodb:UpdateItem",  # Uncomment if you need this action
          "dynamodb:DeleteItem"
        ],
        Resource = aws_dynamodb_table.image_table.arn
      }
    ]
  })
}

# Attach the policy to the Lambda role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_dynamodb_s3_policy.arn
  role       = aws_iam_role.lambda_exec_role.name
}


# Lambda function for handling all API routes using FastAPI
resource "aws_lambda_function" "image_service" {
  function_name = "image_service_lambda"
  handler       = "image_uploader/main.handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_exec_role.arn
  timeout       = 15  # adjust based on your need

  # Assuming the FastAPI app is packaged in a zip file
  filename         = "./archive/image-uploader.zip"
  source_code_hash = filebase64sha256("./archive/image-uploader.zip")

  # Set environment variables if needed
  environment {
    variables = {
      IMAGE_BUCKET   = aws_s3_bucket.image_bucket.bucket
      IMAGE_TABLE    = aws_dynamodb_table.image_table.name
      IMAGE_TAGS_GSI = local.tags-index
      LOGGING_LEVEL  = "debug"
      REGION         = var.region
    }
  }
}
