from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.core.config import settings
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Create the asynchronous engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create the asynchronous sessionmaker
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Dependency to get the database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
