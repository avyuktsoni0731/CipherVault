from flask import Flask, jsonify
from flask_cors import CORS

from encryptor.encryptor import Encryptor

from driveAPI import auth, revoke, get_user_info
from driveFunctions import driveFunctions


app = Flask(__name__)
CORS(app)

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

if __name__ == "__main__":
    app.run(debug=True, port=8080)