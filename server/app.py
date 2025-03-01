# from flask import Flask, jsonify, request, redirect, session
# from flask_cors import CORS
# import tempfile
# from pathlib import Path
# from werkzeug.utils import secure_filename
# from urllib.parse import unquote
# import os
# import time
# from dotenv import load_dotenv

# from encryptor.encryptor import Encryptor

# from driveAPI import auth, revoke, get_user_info
# from driveFunctions import driveFunctions

# load_dotenv()

# app = Flask(__name__)
# app.secret_key = 'avyuktsoni'
# app.config['SESSION_TYPE'] = 'filesystem'
# CORS(app, supports_credentials=True)
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# UPLOAD_FOLDER = '../server/test-data'


# @app.route('/')
# def hello():
#     return jsonify("helloworld")


# # @app.route("/login", methods=["GET", "POST"])
# # def login():
# #     try:
# #         auth()[0]
# #         people_service = auth()[1]
# #         user_info = get_user_info(people_service)
# #         # session['user_info'] = user_info
# #         return jsonify({'status': 'success', 'user_info': user_info}), 200
# #     except Exception as e:
# #         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     try:
#         return auth()  # Now this will redirect for OAuth login if needed
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500


# # New route to handle OAuth callback after the user grants permission
# @app.route("/oauth2callback")
# def oauth2callback():
#     try:
#         # Handles the callback from the Google OAuth flow and stores credentials
#         # return auth()
#         auth()[0]
#         people_service = auth()[1]
#         user_info = get_user_info(people_service)
#         session['user_info'] = user_info
#         return jsonify({'status': 'success', 'user_info': user_info}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# # @app.route("/login", methods=["GET", "POST"])
# # def login():
# #     try:
# #         return auth()  # Now this will redirect for OAuth login if needed
# #     except Exception as e:
# #         return jsonify({'status': 'error', 'message': str(e)}), 500


# # # New route to handle OAuth callback after the user grants permission
# # @app.route("/oauth2callback")
# # def oauth2callback():
# #     try:
# #         # Handles the callback from the Google OAuth flow and stores credentials
# #         return auth()
# #     except Exception as e:
# #         return jsonify({'status': 'error', 'message': str(e)}), 500

# @app.route("/logout", methods=["GET", "POST"])
# def logout():
#     try:
#         revoke()
#         session.clear()
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500

#     return jsonify("logged out")

# @app.route("/api/data", methods=["GET", "POST"])
# def get_data():
#     file_list = driveFunctions.list_files()
#     return jsonify(file_list)


# @app.route("/api/user_info", methods=["GET", "POST"])
# def test_get_user_info():
#     try:
#         _, people_service = auth()
#         user_info = get_user_info(people_service)
#         return jsonify({'status': 'success', 'user_info': user_info}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500



# @app.route('/check-password', methods=["POST"])
# def check_password():
#     try:
#         data = request.get_json()
#         enc_filename = data.get('filename') + '.enc'
#         enc_password = unquote(data.get('password'))
#         print(f'Filename: {enc_filename}\nPassword: {enc_password}')
        
#         output_filename = enc_filename[:-4]
#         download_path = str(Path.home() / "Downloads" / output_filename)

#         file_id = driveFunctions.search_files_by_name(enc_filename)
        
#         temp_file_path = driveFunctions.download_file_from_drive(file_id, enc_filename)

#         print(temp_file_path)
#         print(download_path)
        
#         time.sleep(2)

#         Encryptor.decrypt_file(temp_file_path, enc_password, download_path)

#         os.remove(temp_file_path)
        
#         return jsonify({'success': 'success'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500


# @app.route('/upload', methods=["POST"])
# def upload_file():
#     try:
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part in the request'}), 400
        
#         file = request.files['file']
        
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
        
#         ## driveFunction
#         temp_dir = tempfile.mkdtemp()

#         filename = secure_filename(file.filename)
        
#         temp_file_path = os.path.join(temp_dir, filename)
#         file.save(temp_file_path)
        
#         print(temp_file_path)
#         print(filename)

#         Encryptor.encrypt_file(temp_file_path, temp_file_path)

#         driveFunctions.upload_file_to_drive(temp_file_path + '.enc', filename + '.enc')

#         os.remove(temp_file_path)
#         ##
        
#         return jsonify({'message': 'File Uploaded Successfully'}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    

# @app.route('/api/delete_file', methods=['POST'])
# def delete_file():
#     try:
#         data = request.get_json()
#         filename = data.get('filename') + '.enc'
   
#         print(f'File ID: {filename}')
#         driveFunctions.delete_file(filename)

#         return jsonify({'status': 'success', 'message': 'File deleted successfully'}), 200
#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500


from flask import Flask, jsonify, request, redirect, session
from flask_cors import CORS
import tempfile
from pathlib import Path
from werkzeug.utils import secure_filename
from urllib.parse import unquote
import os
import time
from dotenv import load_dotenv

from encryptor.encryptor import Encryptor
from driveAPI import auth, oauth2callback, get_user_info, revoke
from driveFunctions import driveFunctions

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"
CORS(app, supports_credentials=True)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only for local development

# Define the upload folder
UPLOAD_FOLDER = "../server/test-data"

# Routes
@app.route("/")
def hello():
    return jsonify("helloworld")

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        return auth()  # Redirect to Google's consent page
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/oauth2callback")
def callback():
    try:
        return oauth2callback()  # Handle the OAuth2 callback
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/logout", methods=["GET", "POST"])
def logout():
    try:
        return revoke()  # Revoke the token and clear the session
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/data", methods=["GET", "POST"])
def get_data():
    file_list = driveFunctions.list_files()
    return jsonify(file_list)

@app.route("/api/user_info", methods=["GET", "POST"])
def test_get_user_info():
    try:
        user_info = get_user_info()
        if user_info:
            return jsonify({"status": "success", "user_info": user_info}), 200
        else:
            return jsonify({"status": "error", "message": "User info not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/check-password", methods=["POST"])
def check_password():
    try:
        data = request.get_json()
        enc_filename = data.get("filename") + ".enc"
        enc_password = unquote(data.get("password"))
        print(f"Filename: {enc_filename}\nPassword: {enc_password}")

        output_filename = enc_filename[:-4]
        download_path = str(Path.home() / "Downloads" / output_filename)

        file_id = driveFunctions.search_files_by_name(enc_filename)
        temp_file_path = driveFunctions.download_file_from_drive(file_id, enc_filename)

        print(temp_file_path)
        print(download_path)

        time.sleep(2)

        Encryptor.decrypt_file(temp_file_path, enc_password, download_path)
        os.remove(temp_file_path)

        return jsonify({"success": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # Save the file temporarily
        temp_dir = tempfile.mkdtemp()
        filename = secure_filename(file.filename)
        temp_file_path = os.path.join(temp_dir, filename)
        file.save(temp_file_path)

        # Encrypt and upload the file
        Encryptor.encrypt_file(temp_file_path, temp_file_path)
        driveFunctions.upload_file_to_drive(temp_file_path + ".enc", filename + ".enc")

        # Clean up
        os.remove(temp_file_path)

        return jsonify({"message": "File Uploaded Successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/delete_file", methods=["POST"])
def delete_file():
    try:
        data = request.get_json()
        filename = data.get("filename") + ".enc"
        driveFunctions.delete_file(filename)
        return jsonify({"status": "success", "message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the app
# if __name__ == "__main__":
#     app.run(debug=True)