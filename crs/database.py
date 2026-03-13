import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "recipes.db")

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, 
                                   expire_on_commit=False, 
                                   class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

