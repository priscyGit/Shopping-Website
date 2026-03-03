from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, IntegrityError
import time

from app.db.database import Base, engine

from app.routers.auth_router import router as auth_router
from app.routers.items_router import router as items_router
from app.routers.favorites_router import router as favorites_router
from app.routers.orders_router import router as orders_router
from app.routers.chat_router import router as chat_router


app = FastAPI(title="Hall Decoration Shop")


app.include_router(auth_router)
app.include_router(items_router)
app.include_router(favorites_router)
app.include_router(orders_router)
app.include_router(chat_router)


@app.on_event("startup")
def startup_event():
    retries = 10
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected.")
            break
        except OperationalError:
            print("Database not ready, retrying...")
            retries -= 1
            time.sleep(2)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Database integrity error"}
    )

