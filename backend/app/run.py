from flask import Flask
from backend.app.api.endpoints.notes import notes_bp
from backend.app.api.endpoints.questions import question_bp
from backend.app.api.endpoints.quiz import quiz_bp
from backend.app.api.endpoints.upload import upload_bp
from backend.app.services.s3_service import download_env_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Download the .env file from S3
download_env_file()

# Register Blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(question_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(notes_bp)

if __name__ == '__main__':
    app.run(debug=True)