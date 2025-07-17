import firebase_admin
import requests
import pyrebase
import libbase



# /host/model
# 
def get_host_model_runtime() -> list:
    """
    Get the host model runtime URL from Firebase.
    """
    db = libbase.get_root_db()
    host_list = db.get().get("host/model", None)
    if host_list is None:
        return []
    for host in host_list:
        pass