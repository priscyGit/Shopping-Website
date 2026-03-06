from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.utils.jwt_handler import get_current_user
from app.services.chat_service import get_chat_response   # ← חשוב

router = APIRouter(prefix="/chat", tags=["Chat Assistant"])

@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        result = get_chat_response(user.id, request.message, db)

        return ChatResponse(
            response=result["response"]
        )

    except Exception as e:
        print("Chat error:", e)
        raise HTTPException(status_code=500, detail="AI service error")
