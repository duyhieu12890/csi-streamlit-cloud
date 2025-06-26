import os
import sys
import platform
import streamlit as st

from streamlit_app import sidebar_menu

def get_info():
    return {
        "streamlit_version": st.__version__,
        "python_version": os.sys.version.split()[0],
        "os_info": os.uname().sysname + " " + os.uname().release,
        "system_memory": f"{os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3):.2f} GB",
    }

def check_database():


def status():
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

    st.markdown("""Components:
    - 
    """)

st.set_page_config(
    page_title="Trạng thái ứng dụng",
    layout="centered",
    page_icon="🔧",
)

status()
sidebar_menu()


