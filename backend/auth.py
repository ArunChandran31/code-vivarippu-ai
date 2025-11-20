# backend/auth.py
import firebase_admin
from firebase_admin import credentials, auth as fb_auth
import os

_service_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "./firebase_service_account.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(_service_path)
    firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token: str):
    try:
        decoded = fb_auth.verify_id_token(id_token)
        return decoded  # contains uid, email
    except Exception:
        return None
