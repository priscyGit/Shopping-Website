import streamlit as st
from utils.api import login, register
from utils.auth import init_session, login_user

st.set_page_config(page_title="Login / Register", page_icon="🔐")

init_session()

st.title("Login Page")

tab_login, tab_register = st.tabs(["Login", "Register"])


with tab_login:
    st.subheader("Login")

    username = st.text_input("username ")
    password = st.text_input("password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password")
        else:
            response = login(username, password)
            st.write(response.json())

            if response.status_code == 200:
                user_data = response.json()
                login_user(user_data)
                st.success("Logged in successfully")
                st.switch_page("pages/Orders.py")
            else:
                st.error("username or password is incorrect")


with tab_register:
    st.subheader("Register")

    first_name = st.text_input("Please enter your first name")
    last_name = st.text_input("please enter your last name")
    email = st.text_input("please enter your email")
    phone = st.text_input("please enter your phone number")
    country = st.text_input("please enter your country")
    city = st.text_input("please enter your city")
    username_r = st.text_input("please enter a New username")
    password_r = st.text_input(" please enter a New Password", type="password")

    if st.button("Register "):
        if not all([first_name, last_name, email, username_r, password_r]):
            st.error("Please enter mandatory fields")
        else:
            user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "country": country,
                "city": city,
                "username": username_r,
                "password": password_r
            }

            response = register(user_data)

            if response.ok:
                st.success("Registered successfully")
            else:
                try:
                    data = response.json()
                    st.error(data.get("detail", "Not able to create user"))
                except Exception:
                    st.error(f"Server returned invalid response: {response.text}")


