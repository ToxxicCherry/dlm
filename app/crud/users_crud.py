from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas
from sqlalchemy import select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str) -> models.User:
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> models.User:
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> models.User:
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
