import os
import streamlit as st
from app import sidebar_menu

sidebar_menu()

def settings():
    st.title("Cài đặt ứng dụng")

    st.markdown("""
    Trang này cho phép bạn cấu hình các cài đặt của ứng dụng.
    
    **Các tùy chọn:**
    - Thay đổi ngôn ngữ
    - Cập nhật thông tin người dùng
    - Quản lý thông báo
    """)

    # Placeholder for settings options
    language = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English"])
    notifications = st.checkbox("Nhận thông báo qua email")

    if st.button("Lưu cài đặt"):
        st.success("Cài đặt đã được lưu thành công!")

st.set_page_config(
    page_title="Cài đặt ứng dụng",
    layout="centered",
    page_icon="⚙️"
)
settings()
sidebar_menu()