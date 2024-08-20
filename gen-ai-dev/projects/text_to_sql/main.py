# ignored secrets.toml
import streamlit as st
from openai import OpenAI
from langchain_utils import invoke_chain

st.title("Langchain NL2SQL Chatbot")

# Set OpenAI API key from Streamlit secrets
# client = OpenAI(api_key="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")
# client = OpenAI(api_key="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")
# print(client)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    st.session_state

# Initialize chat history
if "messages" not in st.session_state:
    # print("Creating session state")
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            # response = "I don't know anything"
            response = invoke_chain(prompt,st.session_state.messages)
            # st.markdown(prompt)
            # st.markdown(st.session_state.messages)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    