import os
from datetime import datetime
import uuid

from flask import request, send_file
from image_uploader.services import s3
from image_uploader.services import ddb
from image_uploader.models.image import Image

from image_uploader.commons import constants


def create_file_path(user_id, image_id, file_name):
    return f'{user_id}/{image_id}/{file_name}'


def upload_image(request, user_id):
    image_id = uuid.uuid4()

    file = request.files["file"]

    file_path = create_file_path(user_id, image_id, file.filename)
    # Upload the file to S3 and get the image ID
    # s3.upload_file(file, file_path, constants.IMAGE_BUCKET)

    tags = ''.join(tag.strip(' "[]') for tag in request.form["tags"].split(','))

    image = Image(
        user_id=user_id,
        image_id=image_id.__str__(),
        uploaded_by=user_id,
        uploaded_at=int(datetime.utcnow().timestamp() * 1000),
        size=os.path.getsize(file),
        tags=tags,
        file_path=file_path,
        file_name=file.filename,
        likes=0,
        comments=[]
    )
    print(image)
    # Save the image metadata as a generic model dictionary
    ddb.create_item(image)

    return image


def list_images():
    user_id = request.args.get('userId')  # Returns None if not found
    tag = request.args.get('tag', type=int)
    if user_id:
        ddb.get_item_by_pk(Image(user_id))
    elif tag:
        ddb.get_items_by_gsi_contains(constants.IMAGE_TABLE, constants.IMAGE_TAGS_GSI, "tags", tag)
    else:
        ddb.get_items(constants.IMAGE_TABLE)


def download_image(user_id, image_id):
    image = ddb.get_item(Image(user_id, image_id))
    file_path = create_file_path(user_id, image_id)

    file_name = image.fileName
    file = s3.get_file(file_path, constants.IMAGE_BUCKET)

    # Seek to the beginning of the BytesIO buffer
    file.seek(0)

    # Send the image as a response
    return file, file_name


def delete_image(user_id, image_id):
    image = Image(user_id, image_id)
    ddb.delete_item(image)
    s3.delete_file(create_file_path(user_id, image_id))
