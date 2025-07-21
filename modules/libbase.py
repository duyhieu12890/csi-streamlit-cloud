import firebase_admin
from firebase_admin import credentials, db
import json
import streamlit as st
import pyrebase

def load_firebase():
    print("Loading Firebase...")
    
    # Parse chuỗi JSON từ secrets thành dict
    try:
        firebase_creds = json.loads(st.secrets["FIREBASE_SECRETS_STRING"])

        # Tạo credentials từ dict
        cred = firebase_admin.credentials.Certificate(firebase_creds)

        # Khởi tạo Firebase
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["DATABASE_URL"]
        })
    except ValueError as e:
        print(f"Error parsing Firebase secrets or had initialized app: {e}")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

def auth():
    return pyrebase.initialize_app(json.loads(st.secrets["FIREBASE_CONFIG_STRING"])).auth()


def get_root_db():
    IS_WORK = True
    try:
        load_firebase()
    except Exception as e:
        IS_WORK = False
        print(f"Error getting root database reference: {e}")
        return None
    if IS_WORK:
        print(db.reference("/"))
        return db.reference("/")
    else: return {}

def get_userId_logged():
    if "user" in st.session_state:
        return st.session_state["user"]["localId"]
    return None

def decode_array_from_dict(firebase_dict):
    """
    Chuyển đổi dict dạng Firebase { "0": ..., "1": ... } về list Python.
    Tự động sắp xếp theo key tăng dần.
    """
    if not isinstance(firebase_dict, dict):
        return []

    # Sort theo key số (dù key là str, nhưng cần ép về int để đúng thứ tự)
    return [firebase_dict[k] for k in sorted(firebase_dict.keys(), key=lambda x: int(x))]
