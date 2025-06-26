import os
import streamlit as st
from streamlit_app import sidebar_menu

def login():
    st.title("Đăng nhập")

    st.markdown("""
    Vui lòng đăng nhập để truy cập các tính năng của ứng dụng.
    """)

    # Placeholder for login form
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Đăng nhập"):
        if username == "admin" and password == "password":
            st.success("Đăng nhập thành công!")
            # Redirect to main page or dashboard
        else:
            st.error("Tên đăng nhập hoặc mật khẩu không đúng.")

st.set_page_config(
    page_title="Đăng nhập",
    layout="centered",
    page_icon="🔑"  
)
login()
sidebar_menu(),