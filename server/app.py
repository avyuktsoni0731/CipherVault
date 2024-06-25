from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from encryptor.encryptor import Encryptor

from driveAPI import auth, revoke, get_user_info
from driveFunctions import driveFunctions


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '../server/test-data'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

name_list = []

encryptor = Encryptor()


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
        filename = data.get('filename')
        password = data.get('password')
        print(f'Filename: {filename}\nPassword: {password}')

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
        
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({'message': 'File Uploaded Successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True, port=8080)