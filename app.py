import streamlit as st
import ollama
import yaml

# Load configuration
if "config" not in st.session_state:
    with open("config.yaml", "r") as file:
        st.session_state.config = yaml.safe_load(file)


# Generate chatbot responses
def generate_response():
    stream = ollama.chat(
        model=st.session_state.config["model"], 
        messages=st.session_state.messages, 
        stream=True
    )
    for chunk in stream:
        yield chunk["message"]["content"]


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if prompt := st.chat_input("Say Something"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Assistant response
    with st.chat_message("assistant"):
        response = st.write_stream(generate_response())
    st.session_state.messages.append({"role": "assistant", "content": response})