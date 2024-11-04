from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from .settings import DB_PASSWORD
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://dlm-warehouse_owner:{DB_PASSWORD}@ep-wispy-hat-a2870e3m.eu-central-1.aws.neon.tech/dlm-warehouse'


engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={'ssl': ssl_context})
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
