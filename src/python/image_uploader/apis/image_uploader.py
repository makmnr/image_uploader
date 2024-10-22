from flask import jsonify, request, send_file, Blueprint

from image_uploader.tasks import image_task as task
from image_uploader.commons.logger import logger
from image_uploader.models.image import Image

image_api = Blueprint('image_api', __name__)


@image_api.route('/users/<user_id>/images', methods=['POST'])
def upload_image(user_id):
    logger.info(f"User {user_id} uploading image")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # Call the task to handle image upload logic
    image = task.upload_image(request, user_id)
    return image.__dict__


@image_api.route('/images', methods=['GET'])
def list_images():
    logger.info(f"Lisiting images")

    # Call the task to handle image upload logic
    images = task.list_images()
    images_response = [image.__dict__ for image in images]

    return images_response


@image_api.route('/users/<user_id>/images/<image_id>', methods=['GET'])
def download_image(user_id, image_id):
    file, file_name = task.download_image(user_id, image_id)
    return send_file(file, mimetype='image/jpeg', as_attachment=True, download_name=file_name)


@image_api.route('/users/<user_id>/images/<image_id>', methods=['DELETE'])
def delete_image(user_id, image_id):
    task.delete_image(user_id, image_id)
    return True
