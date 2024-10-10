from flask import jsonify, redirect, url_for, request, session
import os.path
import requests
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive", 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', "openid"]

def get_client_config():
    load_dotenv()
    return {
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


# def auth():

#     creds = None
#     client_config = get_client_config()
    

#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
#         creds = flow.run_local_server(port=2020)

#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         drive_service = build("drive", "v3", credentials=creds)
#         people_service = build("people", "v1", credentials=creds)
        
#         return drive_service, people_service

#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return None
     

def auth():
    creds = None
    client_config = get_client_config()

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_config(client_config, SCOPES)
            # Replace 'http://localhost:2020' with your redirect URI (registered in Google Cloud Console)
            flow = flow.to_web_app(redirect_uri='https://cipher-vault-server.vercel.app/login')
            auth_url, _ = flow.authorization_url()

            # User needs to be redirected to this URL for authorization
            return redirect(auth_url)

    try:
        drive_service = build("drive", "v3", credentials=creds)
        people_service = build("people", "v1", credentials=creds)
        return drive_service, people_service

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def get_user_info(people_service):
    try:
        profile = people_service.people().get(resourceName='people/me', personFields='names,emailAddresses,photos').execute()
        user_info = {
            'name': profile['names'][0]['displayName'],
            'email': profile['emailAddresses'][0]['value'],
            'profile_picture': profile['photos'][0]['url']
        }
        return user_info
    except HttpError as error:
        print(f"An error occurred while fetching user info: {error}")
        return None
        

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
        
    else:
        return jsonify({'status': 'error', 'message': 'Token file not found'}), 404
    

if __name__ == "__main__":
    print(auth()[0])