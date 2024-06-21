from flask import jsonify
import os.path
import requests
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive"]

def auth():
    load_dotenv()

    creds = None
    
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

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=2020)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        
        return service

    except HttpError as error:
        print(f"An error occurred: {error}")
    # print(client_config)
    

def revoke():
    if os.path.exists("token.json"):
        with open("token.json", "r") as token_file:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
        # Revoke the token
        revoke = requests.post(
            'https://oauth2.googleapis.com/revoke',
            params={'token': creds.token},
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )

        if revoke.status_code == 200:
            os.remove("token.json")
            return jsonify({'status': 'success'}), 200
            # print('Token successfully revoked')
        else:
            return jsonify({'status': 'error', 'message': 'Failed to revoke token'}), 500
            # print('An error occurred while revoking the token')
        
    else:
        return jsonify({'status': 'error', 'message': 'Token file not found'}), 404
    

        # Delete the token file
        # print("Token file deleted.")

        
# if __name__ == "__main__":
    # auth()
    # logout()