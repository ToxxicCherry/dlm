from fastapi import FastAPI, Request
from sqlalchemy.orm import Session
from .auth import verify_password
from . import models
from .database import engine, get_db
from .crud import get_user_by_username
from app.routers import users_router, items_router
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from .settings import SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.ext.asyncio import AsyncSession


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app = FastAPI()

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(users_router, prefix="/users", tags=["users"])

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


class BasicAuth(AuthenticationBackend):
    async def authenticate(self, request):
        if 'admin' in request.headers.get('Authorization', ''):
            return True
        return False

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get('username')
        password = form.get('password')

        async with get_db() as db:
            user = await get_user_by_username(db=db, username=username)
            print(user.username)

        if user and user.is_superuser and verify_password(password, user.hashed_password):
            request.session.update({'is_admin': True})
            return True
        return False


auth_backend = BasicAuth(secret_key=SECRET_KEY)
admin = Admin(app, engine, authentication_backend=auth_backend)


class UserAdmin(ModelView, model=models.User):
    column_list = [
        models.User.id,
        models.User.username,
        models.User.email,
        models.User.first_name,
        models.User.last_name,
        models.User.is_admin,
        models.User.is_superuser
    ]


class ItemAdmin(ModelView, model=models.Item):
    column_list = [
        models.Item.id,
        models.Item.name,
        models.Item.description,
        models.Item.quantity,
    ]


admin.add_view(UserAdmin)
admin.add_view(ItemAdmin)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the DLM Warehouse App!"}


@app.on_event('startup')
async def startup_vent():
    await init_db()
