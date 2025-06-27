import os
import sys
import platform
import streamlit as st
import firebase_admin
from firebase_admin import db, credentials, initialize_app
import json
from streamlit_app import sidebar_menu
import streamlit_app as app
import threading
import time
import requests

def get_info():
    return {
        "streamlit_version": st.__version__,
        "python_version": os.sys.version.split()[0],
        "os_info": os.uname().sysname + " " + os.uname().release,
        "system_memory": f"{os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3):.2f} GB",
    }

sign = ["🟡 Waiting", "🔴 Downed", "🟢 Alive", "🔴 Get API Failed", "🟡 Host alive, Runtime not work"]


global IS_FIREBASE_WORK 
global IS_MODEL_HOST_WORK
IS_FIREBASE_WORK = 0
IS_MODEL_HOST_WORK = 0
IS_LLM_HOST_WORK = 0
global host_info



def render_status():
    st.markdown(f"""
    ### Components Important:
    **Firebase API:** `{sign[IS_FIREBASE_WORK]}`  
    **Model Runtime API:** `{sign[IS_MODEL_HOST_WORK]}`  
    **LLM Runtime API:** `{sign[IS_LLM_HOST_WORK]}`  
    
    """)


def try_fetch():
    global IS_FIREBASE_WORK
    global IS_MODEL_HOST_WORK
    global IS_LLM_HOST_WORK
    global host_info

    try:
        ref = db.reference('/')
        data = ref.get()
        IS_FIREBASE_WORK = 2
    except:
        IS_FIREBASE_WORK = 1
    
    # print(IS_FIREBASE_WORK == 2)
    if IS_FIREBASE_WORK == 2:
        ref = db.reference("/url")
        data = ref.get()
        # print(data)
        response = requests.get(
            data['llm'] + "/status",
            timeout=5
        )
        # print(response.status_code)
        if response.status_code == 200:
            result = response.json()
            info_host = result
            print(result)
            IS_MODEL_HOST_WORK = 2
        elif response.status_code == 502:
            IS_MODEL_HOST_WORK = 4
        else:
            IS_MODEL_HOST_WORK = 1
        IS_LLM_HOST_WORK = 3




st.set_page_config(
    page_title="Trạng thái ứng dụng",
    layout="centered",
    page_icon="🔧",
)

if not firebase_admin._apps:
    app.load_firebase()

sidebar_menu()

st.title("Trạng thái ứng dụng")

st.markdown(f"""
Ứng dụng này đang chạy trên nền tảng Streamlit.

### Streamlit Host Information:
**Hê điều hành:** `{get_info()['os_info']}`  
**Phiên bản Streamlit:** `{st.__version__}`  
**Phiên bản Python:** `{get_info()['python_version']}`  
**Bộ nhớ hệ thống:** `{get_info()['system_memory']}`  
**CPU:** `{os.cpu_count()} cores`  
"""
)

standalone_thread = threading.Thread(target=try_fetch)
standalone_thread.start()


placeholder = st.empty()


while True:
    try_fetch()
    with placeholder.container():
        render_status()
    time.sleep(5)