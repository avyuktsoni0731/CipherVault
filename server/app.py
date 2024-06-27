from flask import Flask, jsonify, request
from flask_cors import CORS
import tempfile
from pathlib import Path
from werkzeug.utils import secure_filename
import os

import time

from encryptor.encryptor import Encryptor

from driveAPI import auth, revoke, get_user_info
from driveFunctions import driveFunctions


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '../server/test-data'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

name_list = []

# encryptor = Encryptor()


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        auth()[0]
        people_service = auth()[1]
        user_info = get_user_info(people_service)
        return jsonify({'status': 'success', 'user_info': user_info}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

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


@app.route("/api/user_info", methods=["GET", "POST"])
def test_get_user_info():
    try:
        _, people_service = auth()
        user_info = get_user_info(people_service)
        return jsonify({'status': 'success', 'user_info': user_info}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/check-password', methods=["GET" ,"POST"])
def check_password():
    try:
        data = request.get_json()
        filename = data.get('filename') + '.enc'
        password = data.get('password')
        print(f'Filename: {filename}\nPassword: {password}')

        download_path = str(Path.home() / "Downloads")

        file_id = driveFunctions.search_files_by_name(filename)
        
        temp_file_path = '/private' + driveFunctions.download_file_from_drive(file_id, filename)

        print(temp_file_path)
        
        time.sleep(2)

        Encryptor.decrypt_file(temp_file_path, password, download_path)

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
        
        # file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        
        # print(f'filename: {file.filename}')
        
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
    

if __name__ == "__main__":
    app.run(debug=True, port=8080)