import streamlit as st
import firebase_admin
from firebase_admin import auth as admin_auth
from modules.libbase import auth  # file bạn đang có sẵn pyrebase auth
from modules.libbase import load_firebase
import json
import pyrebase
import os
import streamlit_app as app
import base64

app.sidebar_menu()

# --- Đảm bảo user đã đăng nhập ---
if not st.session_state.get("IS_USER_LOGGED", False):
    st.warning("Bạn cần đăng nhập để truy cập cài đặt.")
    st.stop()

user_info = st.session_state.get("user_info", {})
user_name = st.session_state.get("user_name", "Guest")
user_email = user_info.get("email", "Chưa có email")

st.title("⚙️ Cài đặt tài khoản")

st.markdown(f"**Email đăng nhập:** `{user_email}`")

# --- Đổi tên ---
st.header("📝 Đổi tên hiển thị")
new_name = st.text_input("Tên mới", value=user_name)
if st.button("Cập nhật tên"):
    st.session_state["user_name"] = new_name
    st.success("Tên đã được cập nhật!")

# --- Đổi avatar ---
st.header("🖼️ Đổi avatar")
uploaded_file = st.file_uploader("Tải ảnh mới", type=["jpg", "jpeg", "png"])
if uploaded_file:
    # Encode base64 để lưu tạm thời trong session_state
    encoded = base64.b64encode(uploaded_file.read()).decode()
    st.session_state["user_avatar"] = f"data:image/png;base64,{encoded}"
    st.success("Avatar đã được cập nhật!")

# Hiển thị avatar hiện tại (hoặc mặc định)
st.markdown("### Avatar hiện tại:")
if "user_avatar" in st.session_state:
    st.image(st.session_state["user_avatar"], width=150)
else:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)

# --- Đổi mật khẩu ---
st.header("🔑 Đổi mật khẩu")
current_pw = st.text_input("Mật khẩu hiện tại", type="password")
new_pw = st.text_input("Mật khẩu mới", type="password")
confirm_pw = st.text_input("Nhập lại mật khẩu mới", type="password")

if st.button("Cập nhật mật khẩu"):
    try:
        user = auth.sign_in_with_email_and_password(user_email, current_pw)
        if new_pw == confirm_pw:
            auth.update_user_password(user['idToken'], new_pw)
            st.success("Đổi mật khẩu thành công!")
        else:
            st.error("Mật khẩu mới không khớp.")
    except Exception as e:
        st.error(f"Lỗi: {e}")

# --- Gợi ý thêm: Tùy chỉnh theme ---
st.header("🎨 Tùy chỉnh giao diện (theme)")

themes = ["Sáng", "Tối", "Xanh", "Tím"]
selected_theme = st.selectbox("Chọn theme yêu thích", themes)

if st.button("Áp dụng theme"):
    st.session_state["user_theme"] = selected_theme
    st.success(f"Đã áp dụng theme: {selected_theme}")

# --- Logout ---
if st.button("Đăng xuất"):
    st.session_state["IS_USER_LOGGED"] = False
    st.session_state["user_name"] = "Guest"
    st.session_state["user_info"] = {}
    st.session_state["user_avatar"] = None
    st.success("Bạn đã đăng xuất.")
    st.switch_page("streamlit_app.py")
