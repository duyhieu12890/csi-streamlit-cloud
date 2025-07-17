import os
import streamlit as st
from streamlit_app import sidebar_menu
import pyrebase
import json
import streamlit_app as app
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
import modules.libbase as libbase
import time  
libbase.load_firebase()

st.markdown(
    """
    <h2 style='
        text-align: center; 
        background: linear-gradient(90deg, #38bdf8 0%, #4ade80 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
    '>Chào mừng bạn đến với Health Care!</h2>
    <p style='text-align: center; font-size: 18px; color: #6d28d9;'>
        Nơi bạn có thể theo dõi sức khỏe của mình một cách dễ dàng và hiệu quả.
    </p>
    <hr style='border: 1px solid #a78bfa;'>
    """,
    unsafe_allow_html=True
)



rain(
    emoji="🎉",
    font_size=54,
    falling_speed=5,
    animation_length=1 ,
)

def login():
    name = st.text_input("Tên đăng nhập")
    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")
    re_password = st.text_input("Nhập lại mật khẩu", type="password")

    if st.button("Tạo tài khoản"):    
        if password != re_password:
            st.error("Mật khẩu không khớp!")
        else:
            # try:
                app.auth().create_user_with_email_and_password(email, password)
                st.success("Đăng ký thành công! Vui lòng đăng nhập.")
                time.sleep(2)
                st.switch_page("pages/login.py")
            # except Exception as e:
                # st.error("Lỗi đăng ký: " + str(e))

st.set_page_config(
    page_title="Đăng nhập",
    layout="centered",
    page_icon="🔑",
    initial_sidebar_state="expanded"
)

sidebar_menu()


if st.session_state.get("IS_USER_LOGGED", False):
    st.switch_page("streamlit_app.py")
else:
    login()