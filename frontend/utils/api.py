import requests

BASE_URL = "http://backend:8000"

def login(username, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )

def register(user_data):
    return requests.post(f"{BASE_URL}/auth/register", json=user_data)


def get_all_items():
    return requests.get(f"{BASE_URL}/items")

def search_items(filters: dict):
    return requests.get(f"{BASE_URL}/items/search", params=filters)


def get_favorites(token):
    return requests.get(
        f"{BASE_URL}/favorites",
        headers={"Authorization": f"Bearer {token}"}
    )

def add_to_favorites(item_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(
        f"{BASE_URL}/favorites",
        json={"item_id": item_id},
        headers=headers
    )

def remove_favorite(item_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.delete(
        f"{BASE_URL}/favorites/{item_id}",
        headers=headers
    )


def get_orders(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/orders", headers=headers)

def add_to_order(item_id, quantity, token):
    return requests.post(
        f"{BASE_URL}/orders/add-item",
        json={"item_id": item_id, "quantity": quantity},
        headers={"Authorization": f"Bearer {token}"}
    )


def remove_item_from_order(item_id, quantity, token):
    return requests.post(
        f"{BASE_URL}/orders/remove-item",
        json={"item_id": item_id, "quantity": quantity},
        headers={"Authorization": f"Bearer {token}"}
    )



def purchase_order(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(f"{BASE_URL}/orders/purchase", headers=headers)



def chat_with_assistant(message, token):
    return requests.post(
        f"{BASE_URL}/chat",
        json={"message": message},
        headers={"Authorization": f"Bearer {token}"}
    )

