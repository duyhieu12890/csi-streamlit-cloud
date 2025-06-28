import os
import streamlit as st
import firebase_admin
import json
import pyrebase



def on_init_first():
    if not st.session_state.get("IS_USER_LOGGED", False):
        st.session_state["IS_USER_LOGGED"] = False


def load_firebase():
    # Parse chuỗi JSON từ secrets thành dict
    firebase_creds = json.loads(st.secrets["FIREBASE_SECRETS_STRING"])

    # Tạo credentials từ dict
    cred = firebase_admin.credentials.Certificate(firebase_creds)

    # Khởi tạo Firebase
    firebase_admin.initialize_app(cred, {
        'databaseURL': st.secrets["DATABASE_URL"]
    })

def auth():
    return pyrebase.initialize_app(json.loads(st.secrets["FIREBASE_SECRETS_STRING"])).auth()

def sidebar_menu():
    st.sidebar.image("images/logo.png", use_container_width=True)

    st.sidebar.markdown("<hr style='padding: 0 0 8px 0; margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)

    st.sidebar.page_link("streamlit_app.py", label="Trang chủ", icon="🏠")
    st.sidebar.page_link("pages/status.py", label="Trạng thái ứng dụng", icon="🔧")

    st.sidebar.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #ccc;'/>", unsafe_allow_html=True)



    st.sidebar.markdown("#### Chatbox AI / History")
    st.sidebar.button("Tạo hội thoại mới", key="new_chat_btn", use_container_width=True, icon="➕")

    st.sidebar.status("Loading history...")


    history_box = st.sidebar.empty()

    chat_histories = st.session_state.get("chat_histories", [
        {
            "title": "Hội thoại 1",
            "id": "chat_1",
            "history": [
                {"user": "Bạn", "message": "Xin chào!"},
                {"user": "Bot", "message": "Chào bạn, tôi có thể giúp gì?"},
            ]
        },
        {
            "title": "Hội thoại 2", 
            "id": "chat_2",
            "history": [
                {"user": "Bạn", "message": "Giới thiệu về dự án."},
                {"user": "Bot", "message": "Đây là dự án CSI."}
            ]
        }
    ])    
    # chat_histories = st.session_state.get("chat_histories", [])
    if "selected_chat_idx" not in st.session_state:
        st.session_state["selected_chat_idx"] = 0


    with history_box.container():
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

        if st.sidebar.button("Đăng nhập", key="login_btn", use_container_width=True):
            st.switch_page("pages/login.py")
        
        if st.sidebar.button("Đăng kí", key="signin_btn", use_container_width=True):
            st.switch_page("pages/signin.py")

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
    on_init_first()
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


    is_logged_in = st.session_state.get("is_logged_in", False)
    user_name = st.session_state.get("user_name", "Guest")

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
        
        
        st.info("##### (!)    Bạn chưa đăng nhập. Đăng nhập để sử dụng đầy đủ các tính năng chăm sóc sức khỏe cá nhân.", width="stretch")
    
    else:
        st.title(f"Dashboard Health Care cho {user_name}")

        # Lấy dữ liệu mẫu từ session_state hoặc mặc định
        user_health = st.session_state.get("user_health", {
            "weight": 65,   # kg
            "height": 170,  # cm
            "water": 1500,  # ml
            "calories": 1800, # kcal
            "sleep": 7      # hours
        })

        weight = st.number_input("Cân nặng (kg)", min_value=1, max_value=300, value=user_health["weight"])
        height = st.number_input("Chiều cao (cm)", min_value=50, max_value=250, value=user_health["height"])
        water = st.number_input("Lượng nước đã uống (ml)", min_value=0, max_value=5000, value=user_health["water"])
        calories = st.number_input("Lượng calo đã ăn (kcal)", min_value=0, max_value=10000, value=user_health["calories"])
        sleep = st.number_input("Thời gian ngủ (giờ)", min_value=0.0, max_value=24.0, value=user_health["sleep"], step=0.5)

        # Tính BMI
        bmi = round(weight / ((height / 100) ** 2), 2)
        st.metric("Chỉ số BMI", bmi)

        col1, col2, col3 = st.columns(3)
        col1.metric("Nước đã uống (ml)", water, delta=None)
        col2.metric("Calo đã ăn (kcal)", calories, delta=None)
        col3.metric("Ngủ (giờ)", sleep, delta=None)

        # Lưu lại dữ liệu vào session_state
        st.session_state["user_health"] = {
            "weight": weight,
            "height": height,
            "water": water,
            "calories": calories,
            "sleep": sleep
        }
    
    # st.sidebar.markdown("### Menu")
