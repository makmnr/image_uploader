import os

IMAGE_TABLE = os.getenv("IMAGE_TABLE")  # Get table name from environment variable
IMAGE_BUCKET = os.getenv("IMAGE_BUCKET")  # Get table name from environment variable
IMAGE_TAGS_GSI = os.getenv("IMAGE_TAGS_GSI")  # Get table name from environment variable

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "info")
REGION = os.getenv("REGION", "ap-south-1")
