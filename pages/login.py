import os
import streamlit as st
from streamlit_app import sidebar_menu
import pyrebase
import json
import streamlit_app as app

def login():
    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Tạo tài khoản"):
        try:
            app.auth().create_user_with_email_and_password(email, password)
            st.success("Đăng ký thành công! Vui lòng đăng nhập.")
        except Exception as e:
            st.error("Lỗi đăng ký: " + str(e))

st.set_page_config(
    page_title="Đăng nhập",
    layout="centered",
    page_icon="🔑",
    initial_sidebar_state="expanded"
)

if st.session_state("IS_USER_LOGGED", False):
    st.switch_page("streamlit_app.py")
else:
    login()
sidebar_menu(),