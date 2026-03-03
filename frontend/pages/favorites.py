import streamlit as st
import pandas as pd
from utils.api import get_favorites, remove_favorite
from utils.auth import get_current_user, get_token, is_logged_in,init_session

st.set_page_config(page_title="Favorites", page_icon="⭐")

init_session()

st.title("⭐ Favorite Items")

if not is_logged_in():
    st.warning("You must be logged in to view your favorites.")
    st.stop()

user = get_current_user()
token = get_token()


st.subheader(f"{user['first_name']}'s Favorite Items")

response = get_favorites(token)

try:
    favorites = response.json()
except Exception:
    st.error(f"Server returned invalid response: {response.text}")
    st.stop()

if not isinstance(favorites, list):
    st.error("Invalid favorites format from server.")
    st.stop()

if len(favorites) == 0:
    st.info("You have no favorite items yet.")
    st.stop()

df = pd.DataFrame(favorites)
st.dataframe(df)

st.subheader("Remove Item From Favorites")

selected_item = st.selectbox("Select item to remove", df["name"].tolist())

if st.button("Remove"):
    favorite_id = df[df["name"] == selected_item]["id"].iloc[0]

    response = remove_favorite(favorite_id, token)

    if response.status_code in (200, 204):
        st.success(f"Removed {selected_item} from favorites!")
        st.rerun()
    else:
        try:
            st.error(response.json().get("detail", "Error removing item"))
        except:
            st.error(f"Server error: {response.text}")

