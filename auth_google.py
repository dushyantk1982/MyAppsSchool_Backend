import os
import requests
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Redirect user to Google OAuth
@router.get("/auth/google/login")
def google_login():
    auth_url = (
        f"{GOOGLE_AUTH_URL}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&response_type=code&scope=email%20profile"
    )
    return RedirectResponse(auth_url)

# Handle Google OAuth callback
@router.get("/auth/google/callback")
def google_callback(code : str):
    token_data = {
        "code" : code,
        "client_id" : GOOGLE_CLIENT_ID,
        "client_secret" : GOOGLE_CLIENT_SECRET,
        "redirect_uri" : GOOGLE_REDIRECT_URI,
        "grant_type" : "autherization_code",
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = response.json()
    access_token = token_json.get("access_token")


    # Fetch User info
    user_response = requests.get(
        GOOGLE_USER_INFO_URL, headers={"Autherization": f"Bearer {access_token}"}
    )

    user_info = user_response.json()
    return {"message": "Login Successfully", "user": user_info}


