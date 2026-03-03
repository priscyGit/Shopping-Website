from openai import OpenAI
from sqlalchemy.orm import Session
from app.db.redis_client import redis_client
from app.models.item import Item

API_KEY = "PUT_YOUR_OPENAI_KEY_HERE"
client = OpenAI(api_key=API_KEY)
MAX_PROMPTS = 5

def get_chat_response(user_id: int, message: str, db: Session):
    key = f"chat:{user_id}:count"

    count = redis_client.get(key)
    count = int(count) if count else 0

    if count >= MAX_PROMPTS:
        return {
            "response": "You have reached the limit of 5 prompts for this session.",
            "remaining_prompts": 0
        }

    items = db.query(Item).all()
    items_text = "\n".join([
        f"- {item.name}: ${item.price}, stock: {item.stock}"
        for item in items
    ])

    system_prompt = f"""
You are a shopping assistant.
Here are the available items in the store:
{items_text}
If an item has 0 stock, tell the user it is currently unavailable.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )

        answer = response.choices[0].message.content

    except Exception:
        answer = "AI service error."

    redis_client.set(key, count + 1)

    return {
        "response": answer,
        "remaining_prompts": MAX_PROMPTS - (count + 1)
    }
