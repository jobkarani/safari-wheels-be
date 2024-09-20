from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), 'YOUR_GOOGLE_CLIENT_ID')

        # ID token is valid, get user information from it
        user_email = idinfo['email']
        user_name = idinfo.get('name')
        return {
            'email': user_email,
            'name': user_name,
        }
    except ValueError:
        # Invalid token
        raise Exception("Invalid token")
