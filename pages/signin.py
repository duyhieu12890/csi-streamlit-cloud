import os
import streamlit as st
import streamlit_app as app
import firebase_admin
from firebase_admin import credentials, db

if not firebase_admin._apps:
    app.load_firebase()

app.sidebar_menu()

st.set_page_config(
    page_title="Đăng nhập",
    layout="centered",
    page_icon="🔑",
    initial_sidebar_state="expanded"
)
def signup():

    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Đăng nhập"):
        try:
            user = app.auth().sign_in_with_email_and_password(email, password)
            st.success("Đăng nhập thành công!")
            st.session_state["user"] = user
        except Exception as e:
            st.error("Đăng nhập thất bại!")

if st.session_state("IS_USER_LOGGED", False):
    st.switch_page("streamlit_app.py")
else:
    signup()