import streamlit as st
import pandas as pd
from utils.api import get_all_items, search_items, add_to_favorites, add_to_order
from utils.auth import get_current_user

st.set_page_config(page_title="Main Page", page_icon="🛒")

st.title("🛍️ Shopping Website - Main Page")

user = get_current_user()


st.subheader("Available Items")

response = get_all_items()

try:
    items = response.json()
except Exception:
    st.error(f"Server error: {response.text}")
    st.stop()

if not isinstance(items, list):
    st.error("Invalid items format from server.")
    st.stop()

df = pd.DataFrame(items)


st.subheader("Search Items")

search_name = st.text_input("Search by name (supports multiple words)")
price_filter = st.selectbox("Price filter", ["None", "<", "=", ">"])
price_value = st.number_input("Price value", min_value=0.0, value=0.0)

stock_filter = st.selectbox("Stock filter", ["None", "<", "=", ">"])
stock_value = st.number_input("Stock value", min_value=0, value=0)

if st.button("Search"):
    filters = {
        "name": search_name,
        "price_filter": price_filter,
        "price_value": price_value,
        "stock_filter": stock_filter,
        "stock_value": stock_value
    }

    response = search_items(filters)

    try:
        items = response.json()
    except Exception:
        st.error(f"Server returned invalid response: {response.text}")
        st.stop()

    if len(items) == 0:
        st.warning("No items found.")
    else:
        df = pd.DataFrame(items)


st.dataframe(df)

item_map = {item["name"]: item["id"] for item in items}

selected_item = st.selectbox("Select item", df["name"].tolist())
quantity = st.number_input("Quantity", min_value=1, value=1)

col1, col2 = st.columns(2)

with col1:
    if st.button("Add to Favorites"):
        item_id = item_map[selected_item]
        token = st.session_state.get("token")
        response = add_to_order(item_id, quantity, token)


        if response.status_code == 200:
            st.success("Item added to favorites!")
        else:
            try:
                st.error(response.json().get("detail", "Error adding to favorites"))
            except:
                st.error(f"Server error: {response.text}")

with col2:
    if st.button("Add to Order"):
        item_id = item_map[selected_item]
        token = st.session_state.get("token")
        response = add_to_order(item_id, quantity, token)

        if response.status_code == 200:
            st.success(f"Added {quantity} × {selected_item} to order!")
        else:
            try:
                st.error(response.json().get("detail", "Error adding to order"))
            except:
                st.error(f"Server error: {response.text}")




