# from flask import jsonify, redirect, url_for, request, session
# import os.path
# import requests
# from dotenv import load_dotenv

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import Flow

# from googleapiclient.errors import HttpError

# SCOPES = ["https://www.googleapis.com/auth/drive", 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', "openid"]

# def get_client_config():
#     load_dotenv()
#     return {
#         "web": {
#             "client_id": os.getenv("CLIENT_ID"),
#             "project_id": os.getenv("PROJECT_ID"),
#             "auth_uri": os.getenv("AUTH_URI"),
#             "token_uri": os.getenv("TOKEN_URI"),
#             "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
#             "client_secret": os.getenv("CLIENT_SECRET"),
#             "redirect_uris": os.getenv("REDIRECT_URIS").split(","),
#             "javascript_origins": os.getenv("JAVASCRIPT_ORIGINS").split(","),
#         }
#     }


# # def auth():

# #     creds = None
# #     client_config = get_client_config()
    

# #     if os.path.exists("token.json"):
# #         creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# #     if not creds or not creds.valid:
# #         if creds and creds.expired and creds.refresh_token:
# #             creds.refresh(Request())
# #         else:
# #             flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
# #         # creds = flow.run_local_server(port=2020)
# #             flow.redirect_uri = url_for('oauth2callback', _external=True)
            
# #             # Create the authorization URL to redirect the user to Google's consent screen
# #             authorization_url, state = flow.authorization_url(
# #                 access_type='offline', include_granted_scopes='true'
# #             )
# #             session['state'] = state
# #             return redirect(authorization_url)

# #         # with open("token.json", "w") as token:
# #         #     token.write(creds.to_json())

# #     try:
# #         drive_service = build("drive", "v3", credentials=creds)
# #         people_service = build("people", "v1", credentials=creds)
        
# #         return drive_service, people_service

# #     except HttpError as error:
# #         print(f"An error occurred: {error}")
# #         return None
     
     
# # Authentication and credential handling
# def auth():
#     creds = None
#     client_config = get_client_config()

#     # Check if credentials are available in session
#     if 'credentials' in session:
#         creds = Credentials(**session['credentials'])

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             # Initiate OAuth 2.0 Flow
#             flow = Flow.from_client_config(client_config, SCOPES)
#             flow.redirect_uri = url_for('oauth2callback', _external=True)
            
#             # Generate the authorization URL and save state in the session
#             authorization_url, state = flow.authorization_url(
#                 access_type='offline',
#                 include_granted_scopes='true'
#             )
#             session['state'] = state
#             return redirect(authorization_url)

#     try:
#         # Build the Google Drive and People API services
#         drive_service = build("drive", "v3", credentials=creds)
#         people_service = build("people", "v1", credentials=creds)

#         return drive_service, people_service

#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return None

# # OAuth callback to handle the token exchange
# def oauth2callback():
#     state = session['state']
#     client_config = get_client_config()
    
#     # Handle the OAuth flow and exchange authorization code for credentials
#     flow = Flow.from_client_config(client_config, SCOPES, state=state)
#     flow.redirect_uri = url_for('oauth2callback', _external=True)

#     authorization_response = request.url
#     flow.fetch_token(authorization_response=authorization_response)

#     # Store the credentials in the session for future requests
#     creds = flow.credentials
#     session['credentials'] = {
#         'token': creds.token,
#         'refresh_token': creds.refresh_token,
#         'token_uri': creds.token_uri,
#         'client_id': creds.client_id,
#         'client_secret': creds.client_secret,
#         'scopes': creds.scopes
#     }

#     return redirect(url_for('get_data'))  # Redirect after successful login


# def get_user_info(people_service):
#     try:
#         profile = people_service.people().get(resourceName='people/me', personFields='names,emailAddresses,photos').execute()
#         user_info = {
#             'name': profile['names'][0]['displayName'],
#             'email': profile['emailAddresses'][0]['value'],
#             'profile_picture': profile['photos'][0]['url']
#         }
#         return user_info
#     except HttpError as error:
#         print(f"An error occurred while fetching user info: {error}")
#         return None
        

# # def revoke():
# #     if os.path.exists("token.json"):
# #         with open("token.json", "r") as token_file:
# #             creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
# #         # Revoke the token
# #         revoke = requests.post(
# #             'https://oauth2.googleapis.com/revoke',
# #             params={'token': creds.token},
# #             headers={'content-type': 'application/x-www-form-urlencoded'}
# #         )

# #         if revoke.status_code == 200:
# #             os.remove("token.json")
# #             return jsonify({'status': 'success'}), 200
# #             # print('Token successfully revoked')
# #         else:
# #             return jsonify({'status': 'error', 'message': 'Failed to revoke token'}), 500
        
# #     else:
# #         return jsonify({'status': 'error', 'message': 'Token file not found'}), 404
    
# # Revoke OAuth credentials
# def revoke():
#     if 'credentials' in session:
#         creds = Credentials(**session['credentials'])

#         # Revoke the token
#         revoke_response = requests.post(
#             'https://oauth2.googleapis.com/revoke',
#             params={'token': creds.token},
#             headers={'content-type': 'application/x-www-form-urlencoded'}
#         )

#         if revoke_response.status_code == 200:
#             session.clear()  # Clear the session after successful token revocation
#             return jsonify({'status': 'success'}), 200
#         else:
#             return jsonify({'status': 'error', 'message': 'Failed to revoke token'}), 500
#     else:
#         return jsonify({'status': 'error', 'message': 'Credentials not found in session'}), 404



# if __name__ == "__main__":
#     print(auth()[0])

from flask import jsonify, redirect, url_for, request, session
import os
import requests
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# Define the required scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

def get_client_config():
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

def auth():
    # Initialize the OAuth2 flow
    flow = Flow.from_client_config(
        get_client_config(),
        scopes=SCOPES,
        redirect_uri=os.getenv("REDIRECT_URIS").split(",")[0]  # Use the first redirect URI
    )

    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    # Save the state in the session
    session["state"] = state

    # Redirect the user to the authorization URL
    return redirect(authorization_url)

def oauth2callback():
    # Retrieve the state from the session
    state = session.get("state")
    if not state:
        return jsonify({"status": "error", "message": "State not found in session"}), 400

    # Initialize the OAuth2 flow
    flow = Flow.from_client_config(
        get_client_config(),
        scopes=SCOPES,
        state=state,
        redirect_uri=os.getenv("REDIRECT_URIS").split(",")[0]  # Use the first redirect URI
    )

    # Fetch the token using the authorization response
    flow.fetch_token(authorization_response=request.url)

    # Store the credentials in the session
    creds = flow.credentials
    session["credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }

    return redirect(url_for("get_data"))  # Redirect to the data route after successful login

def get_user_info():
    if "credentials" not in session:
        return None

    # Load credentials from the session
    creds = Credentials(**session["credentials"])

    try:
        # Build the People API service
        people_service = build("people", "v1", credentials=creds)

        # Fetch the user's profile information
        profile = people_service.people().get(
            resourceName="people/me",
            personFields="names,emailAddresses,photos"
        ).execute()

        # Extract and return the user info
        user_info = {
            "name": profile["names"][0]["displayName"],
            "email": profile["emailAddresses"][0]["value"],
            "profile_picture": profile["photos"][0]["url"],
        }
        return user_info

    except HttpError as error:
        print(f"An error occurred while fetching user info: {error}")
        return None

def revoke():
    if "credentials" not in session:
        return jsonify({"status": "error", "message": "Credentials not found in session"}), 404

    # Load credentials from the session
    creds = Credentials(**session["credentials"])

    # Revoke the token
    revoke_response = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": creds.token},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )

    if revoke_response.status_code == 200:
        session.clear()  # Clear the session after successful token revocation
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to revoke token"}), 500