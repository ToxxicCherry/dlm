from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import users_router, items_router
from app.settings import SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app = FastAPI()

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

admin = Admin(engine=engine, title='Admin panel')
admin.add_view(ModelView(models.User))
admin.add_view(ModelView(models.Item))
admin.add_view(ModelView(models.Product))
admin.add_view(ModelView(models.ProductTemplate))
admin.add_view(ModelView(models.ProductTemplateItem))
admin.mount_to(app)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the DLM Warehouse App!"}


@app.on_event('startup')
async def startup_vent():
    await init_db()
