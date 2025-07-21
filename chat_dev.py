import streamlit as st
import os
import google.generativeai as genai
import modules.libbase as libbase

database = libbase.get_root_db()
if database is None:
    st.error("Không thể kết nối đến cơ sở dữ liệu Firebase. Vui lòng kiểm tra cấu hình.")
    st.stop()

class GOOGLE_GEMINI_AI():
    def __init__(self, model) -> None:
        google_apt_key = st.secrets.get("GOOGLE_GEMINI_API","GOOGLE_GEMINI_API")
        self.model = genai.Model(model)
        genai.configure(api_key=google_apt_key)
    
    def generate_messages(self, messages):
        return self.model.generate_content(messages)

class HU