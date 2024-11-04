from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from dotenv import load_dotenv
from urllib.parse import urlparse
import ssl
import os

load_dotenv()

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}"


engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={'ssl': ssl_context})
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
