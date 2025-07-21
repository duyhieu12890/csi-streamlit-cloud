import streamlit as st
from streamlit_app import sidebar_menu
import google.generativeai as genai
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown
import pyrebase
import modules.libbase as libbase
import copy
import hashlib
import time

sidebar_menu()

libbase.load_firebase()

if not st.session_state.get("IS_USER_LOGGED", False):
    st.warning("Bạn cần đăng nhập để sử dụng chatbox.")
    st.stop()

database = libbase.get_root_db()
if database is None:
    st.error("Không thể kết nối đến cơ sở dữ liệu Firebase. Vui lòng kiểm tra cấu hình.")
    st.stop()

google_api_key = st.secrets.get("GOOGLE_GEMINI_API", "GOOGLE_GEMINI_API")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

genai.configure(api_key=google_api_key)

system_base = """Bạn là Health Care AI. Bạn là một chuyên gia về health và food, hãy trả lời các câu hỏi về sức khỏe, dinh dưỡng tương đương.
    Hãy trả lời dễ hiểu. Tránh sử dụng từ ngữ chuyên ngành y khoa phức tạp.
    Bạn có thể trả lời các câu hỏi về:
    - Chế độ ăn uống lành mạnh
    - Lời khuyên về dinh dưỡng
    - Cách duy trì lối sống lành mạnh
    - Các mẹo tập thể dục
    - Cách quản lý căng thẳng
    - Các vấn đề sức khỏe phổ biến
    ...

    Không trả lời các câu hỏi ngoài phạm vi sức khỏe, y tế và dinh dưỡng.
    """

system_extras = []

# Khởi tạo st.session_state.messages nếu nó chưa tồn tại
if "messages" not in st.session_state:
    st.session_state.messages = []

messages = st.session_state.get("messages", [])

# get_history = libbase.get_root_db()[f"/users/{libbase.get_userId_logged()}/chat_history"].get()
user_interaction = st.session_state.get("chatbox_switch_from", None)
st.session_state["history"] = []
if user_interaction == "create_new_chat":
    pass
elif user_interaction == "switch_from_dashboard":
    system_extras.append(f"""\nNgười dùng đã import Dashboard vào Chat. Hãy tiếp tục hỗ trợ họ với các câu hỏi về sức khỏe và dinh dưỡng.
        - Cấu trúc của data như sau: data[metric(Ví dụ cân nặng, chiều cao, huyết áp,...)][Năm][Tháng][Ngày] = Giá trị
        - Data như sau: 
        {libbase.get_root_db()["users"][libbase.get_userId_logged()]["dashboard"]}
        """)
elif user_interaction == "switch_from_history":
    pass
elif user_interaction == "switch_from_classify":
    system_extras.append("""\nNgười dùng đã import Classify vào Chat. Hãy tiếp tục hỗ trợ họ với các câu hỏi về sức khỏe và dinh dưỡng.
        - Cấu trúc của data như sau: data[metric(Ví dụ cân nặng, chiều cao, huyết áp,...)][Năm][Tháng][Ngày] = Giá trị
        - Data như sau: {st.session_state.get("classify_data", "Chưa có dữ liệu nào được nhập.")}
        """
    )

model = genai.GenerativeModel(
    model_name="gemma-3-12b-it",
    system_instruction=system_base
)
chat = model.start_chat(history=st.session_state["history"])

def generate_chat_id(user_uid: str) -> str:
    timestamp = str(int(time.time()))
    raw = f"{timestamp}-{user_uid}-chatbox"
    return hashlib.md5(raw.encode()).hexdigest()

def append_chat_message(chat_id, new_message: dict):
    ref = libbase.get_

IS_FIRST_PROMPT = False
user_prompt = st.chat_input("Start typing a prompt")
chatId = ""
for index, chat_item in enumerate(st.session_state["history"]):
    with st.chat_message("user", avatar="user"):
        st.markdown(user_prompt)
    response = chat.send_message(user_prompt).text
    with st.chat_message("ai", avatar="assistant"):
        st.markdown(response)

    if not IS_FIRST_PROMPT:
        chatId = generate_chat_id()
    database.child("users").child(libbase.get_userId_logged()).child("history").child(chatId).set(libbase
        .decode_array_from_dict(libbase.get_root_db()
            .get()["users"][libbase.get_userId_logged()]
            .get("history")
        )
        .append({"role": "user","parts": user_prompt})
    )

    database.child("users").child(libbase.get_userId_logged()).child("history").child(chatId).set(libbase
        .decode_array_from_dict(libbase.get_root_db()
            .get()["users"][libbase.get_userId_logged()]
            .get("history")
        )
        .append({"role": "user","parts": user_prompt})
    )

    IS_FIRST_PROMPT = True
st.set_page_config(
    page_title="Chat with AI",
    layout="centered",
    page_icon="💬",
)
sidebar_menu()