provider "aws" {
  region = var.region
}

# S3 bucket for image storage
resource "aws_s3_bucket" "image_bucket" {
  bucket = "${var.environment}-${var.region}-${var.image_upload_bucket}"
}