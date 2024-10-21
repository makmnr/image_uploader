from flask import Flask
import awsgi

from image_uploader.apis.image_uploader import image_api

app = Flask(__name__)

app.register_blueprint(image_api)

if __name__ == '__main__':
    app.run(debug=True)


def handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})

# from io import BytesIO
#
# from image_uploader.main import handler
#
#
# # Mock context for testing
# class MockContext:
#     def __init__(self):
#         self.aws_request_id = '1234567890'
#         self.function_name = 'mock_function'
#         self.memory_limit_in_mb = 128
#         self.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:mock_function'
#
# # Path to the local image file
# file_path = "/Users/manju/M/Workspace/M/github/image_uploader/src/python/image_uploader/__init__.py"
#
# # Read the local file as binary
# with open(file_path, "rb") as image_file:
#     binary_data = image_file.read()
#
# # Prepare the multipart form-data body
# boundary = '---011000010111000001101001'
# body = (
#     f'{boundary}\r\n'
#     'Content-Disposition: form-data; name="file"; filename="test_image.jpg"\r\n'
#     'Content-Type: image/jpeg\r\n\r\n'
# )
# # Add the binary data and closing boundary
# body += binary_data.decode('latin-1') + f'\r\n{boundary}--\r\n'  # Decode to handle binary data
#
# # Mock event for file upload to /users/<user_id>/images
# user_id = '12345'  # Replace with your desired user ID
# mock_event = {
#     "httpMethod": "POST",
#     "path": f"/users/{user_id}/images",
#     "headers": {
#         "Content-Type": f"multipart/form-data; boundary={boundary}",
#     },
#     "body": body,
#     "isBase64Encoded": False,
#     "queryStringParameters": {
#         "example_param": "value"  # Add your expected query parameters here
#     },
# }
#
# mock_context = MockContext()
#
# # Call the handler with mock event and context
# response = handler(mock_event, mock_context)
# print(response)
