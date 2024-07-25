from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import tempfile
from pathlib import Path
from werkzeug.utils import secure_filename
from urllib.parse import unquote
import os
import time
from dotenv import load_dotenv

from encryptor.encryptor import Encryptor

from driveAPI import auth, revoke, get_user_info, SCOPES
from driveFunctions import driveFunctions
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)
CORS(app)

load_dotenv()

UPLOAD_FOLDER = '../server/test-data'

name_list = []

client_config = {
    "web": {
        "client_id": os.getenv("CLIENT_ID"),
        "project_id": os.getenv("PROJECT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uris": os.getenv("REDIRECT_URIS").split(","),
        "javascript_origins": os.getenv("JAVASCRIPT_ORIGINS").split(","),
    }
}

@app.route('/')
def hello():
    return jsonify("helloworld")

@app.route("/oauth2callback")
def oauth2callback():
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return jsonify({'status': 'success', 'message': 'Authorization completed. You can now close this window.'}), 200


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     try:
#         auth()[0]
#         people_service = auth()[1]
#         user_info = get_user_info(people_service)
#         return jsonify({'status': 'success', 'user_info': user_info}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/login", methods=["GET"])
def login():
    creds, auth_url = auth()
    if creds:
        return jsonify({'status': 'success', 'message': 'Already authenticated'}), 200
    else:
        return redirect(auth_url)
    

@app.route("/logout", methods=["GET", "POST"])
def logout():
    try:
        revoke()
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify("logged out")


@app.route("/api/data", methods=["GET", "POST"])
def get_data():
    file_list = driveFunctions.list_files()
    return jsonify(file_list)


# @app.route("/api/user_info", methods=["GET", "POST"])
# def test_get_user_info():
#     try:
#         _, people_service = auth()
#         user_info = get_user_info(people_service)
#         return jsonify({'status': 'success', 'user_info': user_info}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/api/user_info", methods=["GET", "POST"])
def test_get_user_info():
    creds, _ = auth()
    if not creds:
        return jsonify({'status': 'error', 'message': 'Authorization required.'}), 401

    try:
        _, people_service = creds
        user_info = get_user_info(people_service)
        return jsonify({'status': 'success', 'user_info': user_info}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/check-password', methods=["POST"])
def check_password():
    try:
        data = request.get_json()
        enc_filename = data.get('filename') + '.enc'
        enc_password = unquote(data.get('password'))
        print(f'Filename: {enc_filename}\nPassword: {enc_password}')
        
        output_filename = enc_filename[:-4]
        download_path = str(Path.home() / "Downloads" / output_filename)

        file_id = driveFunctions.search_files_by_name(enc_filename)
        
        temp_file_path = driveFunctions.download_file_from_drive(file_id, enc_filename)

        print(temp_file_path)
        print(download_path)
        
        time.sleep(2)

        Encryptor.decrypt_file(temp_file_path, enc_password, download_path)

        os.remove(temp_file_path)
        
        return jsonify({'success': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/upload', methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        ## driveFunction
        temp_dir = tempfile.mkdtemp()

        filename = secure_filename(file.filename)
        
        temp_file_path = os.path.join(temp_dir, filename)
        file.save(temp_file_path)
        
        print(temp_file_path)
        print(filename)

        Encryptor.encrypt_file(temp_file_path, temp_file_path)

        driveFunctions.upload_file_to_drive(temp_file_path + '.enc', filename + '.enc')

        os.remove(temp_file_path)
        ##
        
        return jsonify({'message': 'File Uploaded Successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/delete_file', methods=['POST'])
def delete_file():
    try:
        data = request.get_json()
        filename = data.get('filename') + '.enc'
   
        print(f'File ID: {filename}')
        driveFunctions.delete_file(filename)

        return jsonify({'status': 'success', 'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# if __name__ == "__main__":
#     # app.run(debug=True, port=8080)
#     port = int(os.environ.get('PORT', 8080))
#     app.run(host='0.0.0.0', port=port, debug=True)