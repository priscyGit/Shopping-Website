import streamlit as st
import pandas as pd
from utils.api import get_orders
from utils.auth import is_logged_in, get_token, get_current_user, init_session

st.set_page_config(page_title="Orders", page_icon="📦")
init_session()

st.title("My Chart")

if not is_logged_in():
    st.warning("You must be logged in to view your orders.")
    st.stop()

user = get_current_user()
token = get_token()

st.subheader(f"Orders for {user['first_name']}")

response = get_orders(token)

try:
    orders = response.json()
except Exception:
    st.error(f"Server returned invalid response: {response.text}")
    st.stop()

if not isinstance(orders, list):
    st.error("Invalid orders format from server.")
    st.stop()

if len(orders) == 0:
    st.info("You have no orders yet.")
    st.stop()


temp_orders = [o for o in orders if o["status"] == "TEMP"]
closed_orders = [o for o in orders if o["status"] == "CLOSE"]


if temp_orders:
    st.subheader("🟡 Pending Order (TEMP)")

    temp = temp_orders[0]  # Only one TEMP allowed

    st.write(f"**Order ID:** {temp['id']}")
    st.write(f"**Status:** {temp['status']}")
    st.write(f"**Total Price:** ${temp['total_price']}")
    st.write(f"**Shipping Address:** {temp['shipping_address']}")
    st.write("### Items:")

    df_temp = pd.DataFrame(temp["items"])
    st.dataframe(df_temp)

    if st.button("Open Order Process Page"):
        st.switch_page("pages/order_process.py")

else:
    st.info("You have no pending order.")

st.subheader("🟢 Closed Orders (History)")

if closed_orders:
    for order in closed_orders:
        with st.expander(f"Order #{order['id']} — Total: ${order['total_price']}"):
            st.write(f"**Status:** {order['status']}")
            st.write(f"**Date:** {order['order_date']}")
            st.write(f"**Shipping Address:** {order['shipping_address']}")

            df_items = pd.DataFrame(order["items"])
            st.dataframe(df_items)
else:
    st.info("No closed orders found.")
