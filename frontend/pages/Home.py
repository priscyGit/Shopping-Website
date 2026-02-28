import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Shopping Website", layout="wide")

st.title("🛒 Shopping Website")

def get_all_items():
    response = requests.get(f"{API_URL}/items")
    if response.status_code == 200:
        return response.json()
    return []

def search_items(query):
    response = requests.get(f"{API_URL}/items/search", params={"q": query})
    if response.status_code == 200:
        return response.json()
    return []

def add_to_favorites(item_id, token):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.post(f"{API_URL}/favorites", json={"item_id": item_id}, headers=headers)
    return response.status_code == 200

def add_to_order(item_id, token):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.post(
        f"{API_URL}/orders/add-item",
        json={"item_id": item_id, "quantity": 1},
        headers=headers
    )
    return response.status_code == 200


search_query = st.text_input("🔍 Surch item by name:")

if search_query:
    items = search_items(search_query)
else:
    items = get_all_items()

if items:
    df = pd.DataFrame(items)
    st.dataframe(df)

    for item in items:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{item['name']}** — ${item['price']} — In Stock: {item['stock']}")
        with col2:
            if st.button("Favorites", key=f"fav_{item['id']}"):
                st.success(f" Added to Favorites: {item['name']}")
        with col3:
            if st.button("To Purchase", key=f"order_{item['id']}"):
                st.success(f"Added to chart: {item['name']}")
else:
    st.warning("NO items found")
