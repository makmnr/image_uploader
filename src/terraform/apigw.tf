# API Gateway REST API
resource "aws_api_gateway_rest_api" "images_api" {
  name = "ImageAPI"
}

# API Resource for /images
resource "aws_api_gateway_resource" "images_resource" {
  rest_api_id = aws_api_gateway_rest_api.images_api.id
  parent_id   = aws_api_gateway_rest_api.images_api.root_resource_id
  path_part   = "images"
}

# API Resource for /users
resource "aws_api_gateway_resource" "users_resource" {
  rest_api_id = aws_api_gateway_rest_api.images_api.id
  parent_id   = aws_api_gateway_rest_api.images_api.root_resource_id
  path_part   = "users"
}

# API Resource for /users/{userId}
resource "aws_api_gateway_resource" "user_resource" {
  rest_api_id = aws_api_gateway_rest_api.images_api.id
  parent_id   = aws_api_gateway_resource.users_resource.id
  path_part   = "{userId}"
}

# API Resource for /users/{userId}/images
resource "aws_api_gateway_resource" "user_images_resource" {
  rest_api_id = aws_api_gateway_rest_api.images_api.id
  parent_id   = aws_api_gateway_resource.user_resource.id
  path_part   = "images"
}

# API Resource for /users/{userId}/images/{imageId}
resource "aws_api_gateway_resource" "user_image_resource" {
  rest_api_id = aws_api_gateway_rest_api.images_api.id
  parent_id   = aws_api_gateway_resource.user_images_resource.id
  path_part   = "{imageId}"
}

# POST method for /users/{userId}/images
resource "aws_api_gateway_method" "post_user_images" {
  rest_api_id   = aws_api_gateway_rest_api.images_api.id
  resource_id   = aws_api_gateway_resource.user_images_resource.id
  http_method   = "POST"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.userId" = true
  }
}

# Integration for POST method
resource "aws_api_gateway_integration" "post_user_images_integration" {
  rest_api_id             = aws_api_gateway_rest_api.images_api.id
  resource_id             = aws_api_gateway_resource.user_images_resource.id
  http_method             = aws_api_gateway_method.post_user_images.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.image_service.invoke_arn
}

# GET method for /images
resource "aws_api_gateway_method" "get_images" {
  rest_api_id   = aws_api_gateway_rest_api.images_api.id
  resource_id   = aws_api_gateway_resource.images_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# Integration for GET method
resource "aws_api_gateway_integration" "get_images_integration" {
  rest_api_id             = aws_api_gateway_rest_api.images_api.id
  resource_id             = aws_api_gateway_resource.images_resource.id
  http_method             = aws_api_gateway_method.get_images.http_method
  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.image_service.invoke_arn
}

# GET method for /users/{userId}/images/{imageId} (Download)
resource "aws_api_gateway_method" "get_image" {
  rest_api_id   = aws_api_gateway_rest_api.images_api.id
  resource_id   = aws_api_gateway_resource.user_image_resource.id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.userId"  = true,
    "method.request.path.imageId" = true
  }
}

# Integration for GET method for /users/{userId}/images/{imageId}
resource "aws_api_gateway_integration" "get_image_integration" {
  rest_api_id             = aws_api_gateway_rest_api.images_api.id
  resource_id             = aws_api_gateway_resource.user_image_resource.id
  http_method             = aws_api_gateway_method.get_image.http_method
  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.image_service.invoke_arn
}

# DELETE method for /users/{userId}/images/{imageId}
resource "aws_api_gateway_method" "delete_image" {
  rest_api_id   = aws_api_gateway_rest_api.images_api.id
  resource_id   = aws_api_gateway_resource.user_image_resource.id
  http_method   = "DELETE"
  authorization = "NONE"

  request_parameters = {
    "method.request.path.userId"  = true,
    "method.request.path.imageId" = true
  }
}

# Integration for DELETE method
resource "aws_api_gateway_integration" "delete_image_integration" {
  rest_api_id             = aws_api_gateway_rest_api.images_api.id
  resource_id             = aws_api_gateway_resource.user_image_resource.id
  http_method             = aws_api_gateway_method.delete_image.http_method
  integration_http_method = "DELETE"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.image_service.invoke_arn
}

resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [
    aws_api_gateway_integration.post_user_images_integration,
    aws_api_gateway_integration.get_image_integration,
    aws_api_gateway_integration.get_images_integration,
    aws_api_gateway_integration.delete_image_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.images_api.id
}

resource "aws_api_gateway_stage" "stage" {
  depends_on = [aws_cloudwatch_log_group.log_group]
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.images_api.id
  stage_name    = "v1"
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.images_api.id}/v1"
  retention_in_days = 7
}

resource "aws_api_gateway_method_settings" "settings" {
  rest_api_id = aws_api_gateway_rest_api.images_api.id
  stage_name  = aws_api_gateway_stage.stage.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}
