import time
from openai import OpenAI
import streamlit as st

st.title("estelle 🌟")

def greeting_streamer():
    response = "Hello human 👋. My name is Estelle, and I am a friendly bot. I can help you search flights, calculate your carbon footprint during travel, answer trivia and many other things.\
                    I am always up for chitchat too. Ask away 🙂."
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message("assistant", avatar="🌟"):
        st.write_stream(greeting_streamer())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🌟"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})