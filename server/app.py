from flask import Flask, jsonify, request
from flask_cors import CORS

from encryptor.encryptor import Encryptor

from driveAPI import auth, revoke
from gdrive.driveFunctions import driveFunctions


app = Flask(__name__)
CORS(app)

name_list = []

encryptor = Encryptor()


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        auth()
        return jsonify({'status': 'success'}), 200
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
    name_list = driveFunctions.list_files()
    data = {}
    data.update({"name": name_list})
    return data

if __name__ == "__main__":
    app.run(debug=True, port=8080)