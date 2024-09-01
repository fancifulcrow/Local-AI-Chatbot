import streamlit as st
import ollama
import yaml
import json

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

# Load chat history from a JSON file
with st.sidebar:
    uploaded_file = st.file_uploader("Upload File", type="json")

    if st.button("Load Chat History"):
        if uploaded_file is not None:
            st.session_state.messages = json.load(uploaded_file)
            st.success("Chat history loaded successfully!")
        else:
            st.warning("Please upload a file first.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if prompt := st.chat_input("Say Something"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI Assistant response
    with st.chat_message("assistant"):
        response = st.write_stream(generate_response())
    st.session_state.messages.append({"role": "assistant", "content": response})

# Save chat history to a JSON file
with st.sidebar:
    file_name = st.text_input("Enter save filename", "chat_history")
    if file_name:
        st.download_button(
            label="Save Chat History",
            data=json.dumps(st.session_state.messages),
            file_name=f"{file_name}.json",
            mime="application/json"
        )
    else:
        st.warning("You must enter filename to save")
