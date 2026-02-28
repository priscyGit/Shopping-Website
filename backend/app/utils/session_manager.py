import uuid
from redis import Redis

redis_client = Redis(host="redis", port=6379, decode_responses=True)

SESSION_EXPIRE_SECONDS = 60 * 60  # שעה

def create_session(user_id: int):
    token = str(uuid.uuid4())
    redis_client.set(f"session:{token}", user_id, ex=SESSION_EXPIRE_SECONDS)
    return token

def get_user_id_from_session(token: str):
    return redis_client.get(f"session:{token}")

def delete_session(token: str):
    redis_client.delete(f"session:{token}")
