import boto3
import os

s3 = boto3.client('s3',region_name=os.getenv('AWS_REGION'))

def upload_file_to_s3(file, file_name):
    bucket_name = os.getenv('S3_BUCKET_NAME')
    # TODO path update
    s3_key = f'path/with/date/{file_name}'

    s3.upload_fileobj(file, bucket_name, s3_key)
    return s3_key  # Return the S3 key or a unique identifier for the uploaded file
