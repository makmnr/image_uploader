from io import BytesIO

import boto3
import os

from image_uploader.commons import constants
from image_uploader.commons.logger import logger

s3 = boto3.client('s3', region_name=constants.REGION)


def upload_file(file, key, bucket):
    try:
        logger.info(f"uploading file to S3 {bucket} {key}")
        s3.upload_fileobj(file, bucket, key)
    except Exception as e:
        logger.error("Error uploading S3  file",e)


def get_file(key, bucket_name):
    image_data = BytesIO()
    file_stream = s3.download_fileobj(bucket_name, key, image_data)
    return file_stream  # Return the S3 key or a unique identifier for the uploaded file


def delete_file(key):
    bucket_name = constants.IMAGE_BUCKET
    s3.delete_object(Bucket=bucket_name, Key=key)
