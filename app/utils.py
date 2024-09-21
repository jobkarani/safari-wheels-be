from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend
        CLIENT_ID = "798810994611-fh6tdd71d0imku20opk2pg2d70gurg4b.apps.googleusercontent.com"
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        # If the token is valid, return user information
        return {
            'email': idinfo['email'],
            'name': idinfo.get('name', '')  # Optional field
        }
    except ValueError:
        # Invalid token
        raise ValueError("Invalid token")
