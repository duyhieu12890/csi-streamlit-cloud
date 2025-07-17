import os
import streamlit as st
import streamlit_app as app
import firebase_admin
from firebase_admin import credentials, db
import modules.libbase as libbase
import time

libbase.load_firebase()

    

st.markdown("<h2 style='text-align: center; color: #4F8BF9;'>Chào mừng bạn trở lại</h2>", unsafe_allow_html=True)
st.write("Vui lòng đăng nhập để tiếp tục 🚀")

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
            user = libbase.auth().sign_in_with_email_and_password(email, password)
            st.success("Đăng nhập thành công!")
            st.session_state["user"] = user
            st.session_state["IS_USER_LOGGED"] = True
            st.session_state["IS_FIRST_VISIT"] = False
            print(user)
            time.sleep(1)
            st.switch_page("streamlit_app.py")
        except Exception as e:
            st.error("Đăng nhập thất bại!")

if st.session_state.get("IS_USER_LOGGED", False):
    st.switch_page("streamlit_app.py")
else:
    signup()