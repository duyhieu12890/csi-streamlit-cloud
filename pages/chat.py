import os
import streamlit as st
from streamlit_app import sidebar_menu

def chat():
    st.title("Chat with AI")

    st.markdown("""
    This page allows you to interact with an AI chatbot.
    
    **Features:**
    - Ask questions about the lettuce growth tracker
    - Get insights and predictions based on your queries
    """)

    # Placeholder for chat interface
    user_input = st.text_input("You:", "")
    
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
