from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.session_manager import get_user_id_from_session

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("session_token")
        request.state.user_id = None

        if token:
            user_id = get_user_id_from_session(token)
            if user_id:
                request.state.user_id = int(user_id)

        response = await call_next(request)
        return response
