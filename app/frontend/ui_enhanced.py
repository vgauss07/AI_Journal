import streamlit as st
import requests
from datetime import datetime

from app.config.setting import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

# ----------------------------------------------------
# Setup
# ----------------------------------------------------
logger = get_logger(__name__)

st.set_page_config(
    page_title="AI Agent Advisor",
    layout="wide",
    page_icon="🧠"
)

API_URL = "http://127.0.0.1:9999/chat"

# ----------------------------------------------------
# Session State
# ----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------------------------
# Sidebar – Agent Configuration
# ----------------------------------------------------
with st.sidebar:
    st.markdown("## 🧠 Agent Configuration")

    system_prompt = st.text_area(
        "System Prompt",
        placeholder="Define the role, behavior, constraints of your AI agent…",
        height=120
    )

    selected_model = st.selectbox(
        "Model",
        settings.ALLOWED_MODELS
    )

    allowed_web_search = st.checkbox(
        "Allow Web Search",
        value=False
    )

    if st.button("🆕 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ----------------------------------------------------
# Header
# ----------------------------------------------------
st.markdown("## 🤖 Multi-Agent Advisor")
st.caption("Ask complex questions. The agents collaborate behind the scenes.")

st.divider()

# ----------------------------------------------------
# Chat History
# ----------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------------------------------
# User Input
# ----------------------------------------------------
user_query = st.chat_input("Ask the agent…")

if user_query:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query,
        "timestamp": datetime.utcnow().isoformat()
    })

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],   # keep backend contract
        "allowed_search": allowed_web_search
    }

    # ------------------------------------------------
    # Backend Call
    # ------------------------------------------------
    try:
        logger.info("Sending request to backend")

        with st.chat_message("assistant"):
            with st.spinner("Agents are reasoning..."):
                response = requests.post(API_URL, json=payload, timeout=120)

            if response.status_code == 200:
                agent_response = response.json().get("response", "")
                st.markdown(agent_response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": agent_response,
                    "timestamp": datetime.utcnow().isoformat()
                })

                logger.info("Received response from backend")

            else:
                logger.error(f"Backend error: {response.text}")
                st.error("❌ Backend returned an error")

    except Exception as e:
        logger.exception("Error communicating with backend")
        raise CustomException("Error sending request to backend", e)

# ----------------------------------------------------
# Footer
# ----------------------------------------------------
st.divider()
st.caption("Multi-Agent Advisor • Streamlit Frontend")
