import streamlit as st

def init_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "token" not in st.session_state:
        st.session_state["token"] = None


def login_user(data):
    st.session_state["user"] = data["user"]
    st.session_state["token"] = data["access_token"]


def logout_user():
    st.session_state["user"] = None
    st.session_state["token"] = None


def is_logged_in():
    return st.session_state.get("user") is not None


def get_token():
    return st.session_state.get("token")


def get_current_user():
    return st.session_state.get("user")
