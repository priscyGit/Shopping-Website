import streamlit as st
from utils.api import chat_with_assistant
from utils.auth import is_logged_in, get_token, get_current_user, init_session

st.set_page_config(page_title="Chat Assistant", page_icon="💬")

init_session()

st.title("💬 AI Shopping Assistant")

if not is_logged_in():
    st.warning("You must be logged in to use the chat assistant.")
    st.stop()

user = get_current_user()
token = get_token()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

MAX_MESSAGES = 5

if st.session_state.chat_count >= MAX_MESSAGES:
    st.error("You have reached the limit of 5 messages for this session.")
    st.stop()

st.subheader("Chat History")

if len(st.session_state.chat_history) == 0:
    st.info("Start chatting with the assistant!")
else:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")

st.subheader("Ask a question about the store items")

user_message = st.text_input("Your message:")

if st.button("Send"):
    if not user_message.strip():
        st.warning("Please enter a message.")
    else:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        # Send to backend
        response = chat_with_assistant(user_message, token)

        try:
            data = response.json()
        except Exception:
            st.error(f"Server returned invalid response: {response.text}")
            st.stop()

        if response.status_code != 200:
            st.error(data.get("detail", "Chat assistant error"))
            st.session_state.chat_history.append({"role": "assistant", "content": "AI service error."})
        else:
            assistant_reply = data.get("response", "No response from assistant.")
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
            st.session_state.chat_count += 1

        st.rerun()

st.markdown("---")

if st.button("Reset Chat"):
    st.session_state.chat_history = []
    st.session_state.chat_count = 0
    st.success("Chat reset!")
    st.experimental_rerun()
