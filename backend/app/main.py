from fastapi import FastAPI
from app.db.database import Base, engine
from sqlalchemy.exc import OperationalError
import time

app = FastAPI(title="Hall Decoration Shop")

from app.routers.orders_router import router as orders_router
from app.routers.auth_router import router as auth_router
from app.routers.items_router import router as items_router
from app.routers.favorites_router import router as favorites_router

app.include_router(auth_router)
app.include_router(items_router)
app.include_router(favorites_router)
app.include_router(orders_router)

from app.utils.auth_middleware import AuthMiddleware
app.add_middleware(AuthMiddleware)

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
