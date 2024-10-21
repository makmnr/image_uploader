variable "region" {
  default = "ap-south-1"
}

# S3 bucket for image storage
variable "image_upload_bucket" {
  default = "image-upload-bucket"
}

variable "environment" {
  default = "test"
}

variable "log_level" {
  default = "info"
}