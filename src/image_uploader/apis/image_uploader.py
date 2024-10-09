from flask import Blueprint, request, jsonify
from tasks.image_task import upload_image

image_api = Blueprint('image_api', __name__)


@image_api.route('/images', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Prepare the request data to pass to the task
    request_data = {
        'file_name': file.filename,
        'file_type': request.form.get('fileType'),
        'tags': request.form.getlist('tags'),
        'description': request.form.get('description')
    }

    # Call the task to handle image upload logic
    image = upload_image(request_data)

    return jsonify(image), 200


@image_api.route('/images', methods=['GET'])
def list_images():
    pass


@image_api.route('/images/<image_id>', methods=['GET'])
def get_image(image_id):
   pass


@image_api.route('/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    pass
