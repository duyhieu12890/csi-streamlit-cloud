import os
import streamlit as st
import firebase_admin
import json
import pyrebase
import modules.libbase as libbase
import time

# def history_update():
sidebar = st.container()

global sidebar_menu

def sidebar_chathistory():
    sidebar = st.container()
    with sidebar:
        with st.button("< Quay lại", key="view_history_btn", use_container_width=True):
            return
        st.sidebar.markdown("### Lịch sử hội thoại")
        st.sidebar.button("Tạo hội thoại mới", key="new_chat_btn", use_container_width=True, icon="➕")

        # Placeholder for chat history
        chat_histories = libbase.get_root_db().get()["histories"]
        if not chat_histories:
            st.sidebar.info("Chưa có lịch sử hội thoại nào.")
        else:
            for idx, chat in enumerate(len(chat_histories)-1, -1, -1):
                if st.sidebar.button(chat["title"], key=f"chat_{idx}", use_container_width=True):
                    st.session_state["selected_chat_idx"] = idx
                    st.session_state["IS_USER_LOGGED"] = True
                    st.switch_page("pages/chatbox.py")

def sidebar_menu():
    global sidebar
    sidebar = st.container()

    def main():
        with sidebar:
            st.sidebar.image("images/logo.png", use_container_width=True)
            # st.logo("images/corner_logo.png", use_container_width=True)

            st.sidebar.markdown("<hr style='padding: 0 0 8px 0; margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)

            st.sidebar.page_link("streamlit_app.py", label="Trang chủ", icon="🏠")
            if st.session_state.get("IS_USER_LOGGED", False):
                st.sidebar.page_link("pages/classify.py", label="Phân loại thức ăn", icon="🔎")
                st.sidebar.page_link("pages/dashboard.py", label="Thống kê sức khỏe", icon="📈")
            st.sidebar.page_link("pages/status.py", label="Trạng thái ứng dụng", icon="🔧",)
            st.sidebar.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)


            st.sidebar.markdown("#### Chatbox AI / History", )
            if st.session_state.get("IS_USER_LOGGED", False):
                if st.sidebar.button("Tạo hội thoại mới", key=f"new_chat_btn", use_container_width=True, icon="➕"):
                    st.session_state["chatbox_switch_from"] = "create_new_chat"
                    st.switch_page("pages/chat.py")

                if st.sidebar.button("Xem lịch sử hội thoại >", key="view_history_btn", use_container_width=True):
                    st.session_state["showing_history"] = True
                    st.rerun()
            else:
                st.sidebar.info("Bạn cần đăng nhập để sử dụng tính năng chatbox.", icon="ℹ️")
            
            # st.sidebar.status("Loading history...")

            
            history_box = st.sidebar.empty()

            st.sidebar.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)
            is_logged_in = st.session_state.get("IS_USER_LOGGED", False)
            if not is_logged_in:

                guest_col1, guest_col2 = st.sidebar.columns([1, 3])
                with guest_col1:            
                    if not st.session_state.get("IS_USER_LOGGED", False):
                        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=48)
                    else:
                        st.image(st.session_state["user_avatar"], width=48)
                with guest_col2:
                    st.markdown("## Guest", unsafe_allow_html=True)

                if st.sidebar.button("Đăng nhập", key="login_btn", use_container_width=True):
                    st.switch_page("pages/login.py")
                
                if st.sidebar.button("Đăng kí", key="signin_btn", use_container_width=True):
                    st.switch_page("pages/signin.py")

            else:
                user_name = libbase.get_root_db().child("users").child(libbase.get_userId_logged()).get()["name"]
                user_col1, user_col2 = st.sidebar.columns([1, 3])
                with user_col1:
                    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=48)
                with user_col2:
                    st.markdown(f"## {user_name}")
                
                if st.sidebar.button("Cài đặt", key="settings_btn", use_container_width=True):
                    st.switch_page("pages/settings.py")
    
    def history_mode():
        with sidebar:
            if st.sidebar.button("< Quay lại", key="back_from_history", use_container_width=True):
                st.session_state["showing_history"] = False
                st.rerun()

            st.sidebar.markdown("### Lịch sử hội thoại")

            chat_histories = st.session_state.get("chat_histories", [])
            if not chat_histories:
                st.sidebar.info("Chưa có lịch sử hội thoại nào.")
            else:
                for idx, chat in enumerate(chat_histories):
                    if st.sidebar.button(chat["title"], key=f"chat_{idx}", use_container_width=True):
                        st.session_state["selected_chat_idx"] = idx
                        st.session_state["selected_chat"] = chat
                        st.session_state["IS_USER_LOGGED"] = True
                        st.switch_page("pages/chatbox.py")

    # Lựa chọn chế độ sidebar
    if st.session_state.get("showing_history", False):
        history_mode()
    else:
        main()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Trang chủ",
        layout="wide",
        page_icon="🏠",
        initial_sidebar_state="expanded",
    )

    sidebar_menu()
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1606788075763-0b53d0d03e59?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80');
        background-size: cover;
        background-position: center;
        backdrop-filter: blur(2px);
    }
    </style>
    """, unsafe_allow_html=True)


    is_logged_in = st.session_state.get("IS_USER_LOGGED", False)
    user_name = libbase.get_root_db().get().get(f"users/{libbase.get_userId_logged()}/name", "Guest")

    if not is_logged_in:
        # st.title("🌱 Chào mừng đến với Health Care App!")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6dd5ed, #2193b0); padding: 2rem 1rem; margin-bottom: 1rem; border-radius: 20px;">
            <h1 style="color: white; text-align: center; margin-bottom: 0;">🌱 Health Care App</h1>
            <p style="color: #f0f0f0; text-align: center;">Hành trình chăm sóc sức khỏe thông minh của bạn bắt đầu tại đây.</p>
        </div>
    """, unsafe_allow_html=True)

        home_col1, home_col2 = st.columns([1,3])
        with home_col1:
            st.image("images/health_care_intro.png", width=300, channels="RGB")
        
        with home_col2:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 32px;">
                    <div>
                        <h3 style="margin-bottom: 8px;">Ứng dụng theo dõi sức khỏe cá nhân hiện đại</h3>
                        <ul style="font-size: 1.1em;">
                            <li>👤 Quản lý cân nặng, chiều cao, chỉ số BMI</li>
                            <li>💧 Theo dõi lượng nước uống mỗi ngày</li>
                            <li>🍎 Ghi lại lượng calo tiêu thụ</li>
                            <li>🛌 Quản lý giấc ngủ, cải thiện sức khỏe</li>
                            <li>📈 Xem dashboard trực quan, dễ hiểu</li>
                        </ul>
                        <p style="margin-top: 12px;">Hãy <b>đăng nhập</b> để bắt đầu hành trình chăm sóc sức khỏe của bạn!</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("---")
        
        
        if not st.session_state.get("IS_USER_LOGGED", False):st.info("##### (!)    Bạn chưa đăng nhập. Đăng nhập để sử dụng đầy đủ các tính năng chăm sóc sức khỏe cá nhân.", width="stretch")
    
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43cea2, #185a9d); padding: 2rem 1rem; margin-bottom: 1rem; border-radius: 20px;">
            <h2 style="color: white; text-align: center; margin-bottom: 0;">🎉 Xin chào, <b>{}</b>!</h2>
            <p style="color: #f0f0f0; text-align: center;">Chúc bạn một ngày tràn đầy năng lượng và sức khỏe!</p>
        </div>
        """.format(user_name), unsafe_allow_html=True)

        fun_col1, fun_col2 = st.columns([1, 3])
        with fun_col1:
            st.image("images/health_care_intro.png", width=300, channels="RGB")
        with fun_col2:
            st.success("🌟 Đã đăng nhập thành công! Hãy khám phá các tính năng chăm sóc sức khỏe cá nhân của bạn ở menu bên trái.")
            st.markdown("""
            <ul>
                <li>🔎 <b>Phân loại thức ăn</b>: Khám phá thông tin dinh dưỡng của các món ăn.</li>
                <li>📈 <b>Thống kê sức khỏe</b>: Theo dõi tiến trình và các chỉ số sức khỏe của bạn.</li>
                <li>💬 <b>Chatbox AI</b>: Trò chuyện với AI để nhận tư vấn sức khỏe.</li>
            </ul>
            """, unsafe_allow_html=True)
            st.info("Đừng quên cập nhật thông tin cá nhân để nhận được lời khuyên phù hợp nhất nhé!")
    
    # st.sidebar.markdown("### Menu")
