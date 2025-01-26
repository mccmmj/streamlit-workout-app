import os
import json
import logging
import streamlit as st

from openai import OpenAI

from api import agent_orchestrator
from modals import accept_or_reject_workout_routine

log = logging.getLogger(__name__)

st.title("Fitness Chatbot")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


st.subheader("Your Fitness Profile")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# # Suplementary user input
# note_text = st.text_area(
#     "Enter any health conditions or notes:",
#     placeholder="e.g., knee injury, prefer low-impact exercises")
# notes = note_text.split("\n")

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    user_profile = None \
        if 'shared_user_profile' not in st.session_state \
        else st.session_state.shared_user_profile

    try:
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # stream = "hello world"
            result = agent_orchestrator(prompt)
            log.debug("result: %r", result)
            accept_or_reject_workout_routine(result)
            # response = st.json(json.dumps(result))
            # stream = client.chat.completions.create(
            #     model=st.session_state["openai_model"],
            #     messages=[
            #         {"role": m["role"], "content": m["content"]}
            #         for m in st.session_state.messages
            #     ],
            #     stream=True,
            # )
            # response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": result})

    except Exception as e:
        st.exception(str(e))
