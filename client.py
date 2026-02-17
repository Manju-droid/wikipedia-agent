import requests
import streamlit as st


st.set_page_config(page_title="Wiki-Bot", page_icon="🤖")
st.title("🤖 Email sending Agent")
st.caption("Powered by FastAPI & LangChain")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
   with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask!"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        st.markdown("Searching Wikipedia...")
    response = requests.post("http://localhost:8000/chat/", json={"message": prompt})

    if response.status_code != 200:
        st.error("Error from server: " + response.text)
    else:   
     answer = response.json().get("response")
     st.markdown(answer)
     st.session_state.messages.append({"role": "assistant", "content": answer})        