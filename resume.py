from flask import Flask, request, jsonify
import jwt
import datetime
import boto3
import fitz  # PyMuPDF for PDF parsing
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
import os

app = Flask(__name__)

# Secret key for JWT
app.config['SECRET_KEY'] = 'your_secret_key'

# AWS S3 Config
S3_REGION = "us-east-1"
s3_client = boto3.client('s3')


# Mock user authentication
users = {"admin": "password123"}

# Login route (JWT Authentication)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username in users and users[username] == password:
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                           app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({"message": "Invalid credentials"}), 401

# Upload Resume (S3 Integration)
@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['resume']
    filename = secure_filename(file.filename)
    
    S3_BUCKET = "your-s3-bucket-name"   # 👉 உங்கள் S3 bucket பெயர்
S3_REGION = "us-east-1"  # 👉 உங்கள் AWS Region (பதிவேடு பார்த்து சரிபார்க்கவும்)

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = "your-s3-bucket-name"
S3_REGION = "us-east-1"
s3_client = boto3.client("s3")

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = file.filename
        s3_client.upload_fileobj(file, S3_BUCKET, filename)
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
        
        return jsonify({"message": "File uploaded successfully", "file_url": file_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
