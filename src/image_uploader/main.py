from flask import Flask
from apis.image_uploader import image_api

app = Flask(__name__)

# Register the image API blueprint
app.register_blueprint(image_api)

if __name__ == '__main__':
    app.run(debug=True)
