import io
import re
import streamlit as st
from PIL import Image
import requests
import base64
import uuid

BASE_URL = "http://localhost:5000"
st.set_page_config(page_title="DataTalk", layout="wide", page_icon="altri_logo-Photoroom.png")
# st.title("Analytical Agent")

def get_logo_base64():
    try:
        with open("altri_logo-Photoroom.png", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""
    
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <img src="data:image/png;base64,{}" class="logo-img">
        <div class="separator"></div>
        <div class="text-content">
            <div class="title-text">DataTalk</div>
        </div>
    </div>
</div>
""".format(get_logo_base64()), unsafe_allow_html=True)
    
style = """
<style>
    .stApp {
        background-color: #FDF9F3; /* Light cream background from image */
        min-height: 100vh;
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 2rem 1rem 2rem;
        color: #2D3436;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .logo-img {
        width: 60px;
        height: 60px;
        object-fit: contain;
    }
    
    .separator {
        width: 1px;
        height: 40px;
        background: rgba(0, 0, 0, 0.1);
        margin: 0 0.5rem;
    }
    
    .text-content {
        text-align: left;
    }
    
    .title-text {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        color: #5D967C; /* Sage green from button */
        letter-spacing: -1px;
    }
    
    /* Fix chat input styling */
    .stChatInput {
        padding: 0 2rem !important;
        margin: 0 !important;
        background-color: transparent !important;
    }
    
    .stChatInput > div {
        background-color: transparent !important;
    }

    .stChatInput > div > div {
        background-color: transparent !important;
    }
    
    .stChatInput > div > div > div {
        background: #ffffff !important;
        border-radius: 30px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin: 0 !important;
        width: 100% !important;
        overflow: hidden !important;
    }
    
    .stChatInput input,
    .stChatInput textarea {
        color: #2D3436 !important;
        caret-color: #5D967C !important;
        font-size: 1rem !important;
        padding: 1rem 1.5rem !important;
    }
    
    /* Chat message bubbles */
    .stChatMessage {
        background: transparent !important;
        margin: 1rem auto !important;
        max-width: 70% !important;
        width: 70% !important;
    }
    
    /* Assistant bubble - Sage Greenish */
    .stChatMessage[data-testid*="assistant"] {
        background-color: #F3F8F5 !important; /* Very light sage */
        border: 1px solid #E1EBE6 !important;
        border-radius: 20px 20px 20px 0px !important;
        color: #2D3436 !important;
    }
    
    /* User bubble - Light Gray/White */
    .stChatMessage[data-testid*="user"] {
        background-color: #ffffff !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 20px 20px 0px 20px !important;
        color: #2D3436 !important;
    }
    
    /* Text inside bubbles */
    .stChatMessage p,
    .stChatMessage div,
    .stChatMessage span {
        color: #2D3436 !important;
        font-weight: 400 !important;
        text-shadow: none !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    .stButton button {
        background-color: #5D967C !important; /* Sage green button */
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background-color: #4A7B63 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(93, 150, 124, 0.3) !important;
    }
</style>
"""
st.markdown(style, unsafe_allow_html=True)
st.markdown('<div class="custom-app-header">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if "client_id" not in st.session_state:
    st.session_state.client_id = str(uuid.uuid4())

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []


def reset_conversation():
    st.session_state.messages = []
    requests.delete(f"{BASE_URL}/clear/{st.session_state.session_id}")
    st.session_state.session_id = str(uuid.uuid4()) 
    show_chat()


def log_error(error: Exception):
    with open("error.log", "a+") as logf:
        logf.write(str(error) + "\n")


def generate_response(question):
    try:
        query_request_with_session = {
            "question": question,
            "session_id": st.session_state.client_id,
        }
        response = requests.post(
            f"{BASE_URL}/query",
            json=query_request_with_session,
            headers={"Content-Type": "application/json"},
        )
        data = response.json()
        ai_response = data["answer"]
        visualization = data.get("visualization", None)
    except Exception as err:
        log_error(err)

        return str(err), None

    return ai_response, visualization


def show_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["type"] == "image":
                image = Image.open(io.BytesIO(message["content"]))
                st.image(image, caption="Generated Plot", width=600)
            else:
                st.markdown(message["content"])


# Render chat history
show_chat()

# Handle new input
if prompt_input := st.chat_input():
    # Add user input to chat
    st.session_state.messages.append(
        {"role": "user", "content": prompt_input, "type": "text"}
    )

    with st.chat_message("user"):
        st.markdown(prompt_input)

    with st.spinner("Wait for it...", show_time=True):
        answer, visualization = generate_response(prompt_input)

    # Add assistant's answer
    if visualization:
        answer = answer.replace("[IMAGE_DATA:]", "").strip()

    if answer:
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "type": "text"}
        )
        with st.chat_message("assistant"):
            st.markdown(answer)

    # Add image if visualization is present
    if visualization:
        for base64_str in visualization["image_base64"]:
            try:
                # Remove base64 prefix if present
                if base64_str.startswith("data:image"):
                    base64_str = re.sub("^data:image/.+;base64,", "", base64_str)

                # Decode base64 string
                image_bytes = base64.b64decode(base64_str)

                # Add image to session state messages
                st.session_state.messages.append(
                    {"role": "assistant", "content": image_bytes, "type": "image"}
                )

                # Display the image
                with st.chat_message("assistant"):
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption="Generated Plot", width=600)

            except Exception as err:
                log_error(f"[Image decode/render error]: {err}\nBase64 snippet: {base64_str[:100]}...")
                st.error("Failed to load one of the visualization images.")

