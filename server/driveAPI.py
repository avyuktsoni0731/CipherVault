from flask import jsonify
import os.path
import requests
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive", 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', "openid"]

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
            auth_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
            return None, auth_url
        # creds = flow.run_local_server(port=2020)

        # with open("token.json", "w") as token:
        #     token.write(creds.to_json())

    try:
        drive_service = build("drive", "v3", credentials=creds)
        people_service = build("people", "v1", credentials=creds)
        
        return drive_service, people_service, None #new

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None, None #new
    
    
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
    


def fxn():
    try:
        drive_service, people_service = auth()
        user_info = get_user_info(people_service)
        print(user_info)
    except Exception as e:
        print(f"An error occured: {e}")
        
if __name__ == "__main__":
    print(auth()[0])