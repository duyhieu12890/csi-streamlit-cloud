import os
import streamlit as st
from streamlit_app import sidebar_menu
import google.generativeai as genai
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown
import pyrebase
import modules.libbase as libbase

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

model = genai.Model("gemma-3n-e4b-it")

# create_new_chat
# switch_from_dashboard
# switch_from_history
# switch_from_classify
messages_default = [{
    "role": "system",
    "content": """Bạn là Health Care AI. Bạn là một chuyên gia về health và food, hãy trả lời các câu hỏi về sức khỏe, dinh dưỡng tương đương.
    Hãy trả lời dễ hiểu. Tránh sử dụng từ ngữ chuyên ngành y khoa phức tạp.
    Bạn có thể trả lời các câu hỏi về:
    - Chế độ ăn uống lành mạnh
    - Lời khuyên về dinh dưỡng
    - Cách duy trì lối sống lành mạnh
    - Các mẹo tập thể dục
    - Cách quản lý căng thẳng
    - Các vấn đề sức khỏe phổ biến
    ...

    Không trả lời các câu hỏi ngoài phạm vi sức khỏe và dinh dưỡng.
    """
}]

messages = []

get_history = libbase.get_root_db()[f"/users/{libbase.get_userId_logged()}/chat_history"].get()
user_interaction = st.session_state.get("chatbox_switch_from", None)
if user_interaction == "create_new_chat":
    pass
elif user_interaction == "switch_from_dashboard":
    messages.append({
        "role": "system",
        "content": f"""Người dùng đã import Dashboard vào Chat. Hãy tiếp tục hỗ trợ họ với các câu hỏi về sức khỏe và dinh dưỡng.
        - Cấu trúc của data như sau: data[metric(Ví dụ cân nặng, chiều cao, huyết áp,...)][Năm][Tháng][Ngày] = Giá trị
        - Data như sau: 
        
        """})
elif user_interaction == "switch_from_history":
    pass
elif user_interaction == "switch_from_classify":
    messages.append({
        "role": "system",
        "content": f"""Người dùng đã import Classify vào Chat. Hãy tiếp tục hỗ trợ họ với các câu hỏi về sức khỏe và dinh dưỡng.
        - Cấu trúc của data như sau: data[metric(Ví dụ cân nặng, chiều cao, huyết áp,...)][Năm][Tháng][Ngày] = Giá trị
        - Data như sau: {st.session_state.get("classify_data", "Chưa có dữ liệu nào được nhập.")}
        """})
    })



def chat():
    st.title("Chat với AI")

    

    # Placeholder for chat interface
    user_input = st.chat_input("Ask me anything about health or food!")
    
    if user_input:
        # Simulate a response from the AI (this would be replaced with actual AI logic)
        response = f"AI Response to: {user_input}"
        st.write(response)

st.set_page_config(
    page_title="Chat with AI",
    layout="centered",
    page_icon="💬",
)
chat()
sidebar_menu()
