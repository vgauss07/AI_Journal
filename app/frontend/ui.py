import streamlit as st
import requests   # to send http post right in the back end

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title='AI Agent Advisor', layout='centered')
st.title('Multi AI Agent  Advisor')

system_prompt = st.text_area("Define your AI Agent: ", height=70)
selected_model = st.selectbox("Select an AI Model: ", settings.ALLOWED_MODELS)


allowed_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your Query: ", height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allowed_search": allowed_web_search
    }

    # Box to send the backend to the frontend
    try:
        logger.info("Sending Request to the backend")

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            # storing response from backend
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"),
                        unsafe_allow_html=True)

        else:
            logger.error("Backend Error")
            st.error("Error with backend")

    except Exception as e:
        logger.error("Error sending request to backend")
        st.error(str(CustomException("Failed to commmunicate to backend", e)))
