from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import users_router, items_router, products_router
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_):
    await init_db()
    yield


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
app = FastAPI(lifespan=lifespan)

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(products_router, prefix="/products", tags=["products"])
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the DLM Warehouse App!"}
