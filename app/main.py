from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import users_router, items_router, products_router
from app.settings import SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
from contextlib import asynccontextmanager


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(products_router, prefix="/products", tags=["products"])
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

admin = Admin(engine=engine, title='Admin panel')
admin.add_view(ModelView(models.User))
admin.add_view(ModelView(models.Item))
admin.add_view(ModelView(models.Product))
admin.mount_to(app)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the DLM Warehouse App!"}

