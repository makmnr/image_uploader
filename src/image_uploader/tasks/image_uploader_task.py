from services.s3 import upload_file_to_s3
from services.ddb import create_item
from models.image import Image

def upload_image(request_data):
    file = request_data['file']

    # Upload the file to S3 and get the image ID
    image_id = upload_file_to_s3(file, request_data['file'])

    # Create an Image model instance
    image = Image(image_id, request_data['file_name'], request_data['file_type'], request_data['tags'], request_data['description'])

    # Save the image metadata as a generic model dictionary
    create_item(image.to_dict())

    return image

# TODO: other tasks