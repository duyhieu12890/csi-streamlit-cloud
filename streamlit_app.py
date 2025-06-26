import os
import streamlit as st


def sidebar_menu():


    st.sidebar.image("images/mindx_light.png", use_container_width=True)


    st.sidebar.markdown("<hr style='padding: 0 0 8px 0; margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)

    st.sidebar.page_link("app.py", label="Trang chủ", icon="🏠")
    st.sidebar.page_link("pages/status.py", label="Trạng thái ứng dụng", icon="🔧")

    st.sidebar.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)



    st.sidebar.markdown("#### Chatbox AI / History")
    st.sidebar.button("Tạo hội thoại mới", key="new_chat_btn", use_container_width=True, icon="➕")

    chat_histories = st.session_state.get("chat_histories", [
        {"title": "Hội thoại 1",
            "id": "chat_1",
            "history": [
                {"user": "Bạn", "message": "Xin chào!"},
                {"user": "Bot", "message": "Chào bạn, tôi có thể giúp gì?"},
            ]
        },
        {"title": "Hội thoại 2", 
            "id": "chat_2",
            "history": [
                {"user": "Bạn", "message": "Giới thiệu về dự án."},
                {"user": "Bot", "message": "Đây là dự án CSI."}
            ]
        }
    ])
    if "selected_chat_idx" not in st.session_state:
        st.session_state["selected_chat_idx"] = 0



    for idx, chat in enumerate(chat_histories):
        if st.sidebar.button(chat["title"], key=f"chat_{idx}", use_container_width=True):
            st.session_state["selected_chat_idx"] = idx

    st.sidebar.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)
    is_logged_in = st.session_state.get("is_logged_in", False)
    user_name = st.session_state.get("user_name", "Guest")
    if not is_logged_in:

        guest_col1, guest_col2 = st.sidebar.columns([1, 3])
        with guest_col1:            
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=48)
        with guest_col2:
            st.markdown("## Guest", unsafe_allow_html=True)

        if st.sidebar.button("Đăng nhập / Đăng ký", key="login_signup_btn", use_container_width=True):
            st.switch_page("pages/login.py")
    else:
        user_col1, user_col2 = st.sidebar.columns([1, 3])
        with user_col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=48)
        with user_col2:
            st.markdown(f"**{user_name}**")
        
        if st.sidebar.button("Xem thông tin cá nhân", key="profile_btn", use_container_width=True):
            st.switch_page("pages/profile.py")
        if st.sidebar.button("Cài đặt", key="settings_btn", use_container_width=True):
            st.switch_page("pages/settings.py")


if __name__ == "__main__":
    st.set_page_config(
        page_title="Trang chủ",
        layout="wide",
        page_icon="🏠",
        initial_sidebar_state="expanded",
    )

    sidebar_menu()
    
    st.title("Trang chủ")
    st.write("Chào mừng bạn đến với ứng dụng của chúng tôi!")
    
    
    # st.sidebar.markdown("### Menu")
