import streamlit as st
import pandas as pd
from utils.api import (
    get_orders,
    add_to_order,
    remove_item_from_order,
    purchase_order,
    get_all_items
)
from utils.auth import is_logged_in, get_token, get_current_user, init_session

st.set_page_config(page_title="Order Process", page_icon="📝")

init_session()

st.title("📝 Order Process")

if not is_logged_in():
    st.warning("You must be logged in to manage your order.")
    st.stop()

user = get_current_user()
token = get_token()

response = get_orders(token)
orders = response.json()

temp_orders = [o for o in orders if o["status"] == "TEMP"]

if not temp_orders:
    st.info("You have no pending order.")
    st.stop()

order = temp_orders[0]

st.subheader(f"Pending Order #{order['id']}")

# הצגת פריטים בהזמנה
if order["items"]:
    df = pd.DataFrame(order["items"])
    st.dataframe(df)
else:
    st.warning("Your order is empty. Add items from the Main Page.")
    st.stop()

# REMOVE ITEM
st.subheader("Remove Item From Order")

selected_item = st.selectbox("Select item to remove", df["name"].tolist())

row = df[df["name"] == selected_item].iloc[0]
item_id = int(row["item_id"])
max_quantity = int(row["quantity"])

remove_qty = st.number_input(
    "How many units to remove?",
    min_value=1,
    max_value=max_quantity,
    value=1,
    step=1
)

if st.button("Remove Item"):
    response = remove_item_from_order(item_id, remove_qty, token)

    if response.status_code == 200:
        st.success(f"Removed {remove_qty} × {selected_item} from order!")
        st.rerun()
    else:
        st.error(response.json().get("detail", "Error removing item"))




# ADD ITEM
st.subheader("Add Item to Order")

items_response = get_all_items()
all_items = items_response.json()

item_map = {item["name"]: item["id"] for item in all_items if item["stock"] > 0}

if not item_map:
    st.info("No items available in stock.")
else:
    item_to_add = st.selectbox("Select item to add", list(item_map.keys()))

    quantity_to_add = st.number_input(
        "Quantity to add",
        min_value=1,
        step=1
    )

    if st.button("Add Item"):
        item_id = item_map[item_to_add]
        response = add_to_order(item_id, quantity_to_add, token)
        st.rerun()

# SUMMARY
st.subheader("Order Summary")

st.write(f"**Total Price:** ${order['total_price']}")
st.write(f"**Shipping Address:** {order['shipping_address']}")

if order["items"]:
    if st.button("Purchase Order"):
        response = purchase_order(token)
        st.success("Order purchased successfully!")
        st.switch_page("pages/Orders.py")
