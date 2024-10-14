from fastapi import FastAPI
from . import models
from .database import engine
from app.routers import users_router, items_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the DLM Warehouse App!"}
