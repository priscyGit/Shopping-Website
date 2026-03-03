from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.models.item import Item

router = APIRouter(prefix="/chat", tags=["Chat Assistant"])

@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        message = request.message.lower()

        # חיפוש פריט לפי שם
        item = db.query(Item).filter(Item.name.ilike(f"%{message}%")).first()

        if item:
            return ChatResponse(
                response=f"There are {item.stock} units of {item.name} in stock."
            )

        # תשובה ברירת מחדל
        return ChatResponse(
            response="I can answer questions about store items only."
        )

    except Exception as e:
        print("Chat error:", e)
        raise HTTPException(status_code=500, detail="AI service error")
