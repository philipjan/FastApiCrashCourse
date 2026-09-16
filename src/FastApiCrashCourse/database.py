import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DBManager:
    def __init__(self):
        self.db_engine =  create_async_engine(url=os.getenv("POSTGRES_BASE_URL"))
        self.__sql_alchemy_base = Base

        # schema creation now runs in the FastAPI lifespan via run_sync
        self.__db_session = async_sessionmaker(
            bind=self.db_engine,
            autoflush=False,
            autocommit=False,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_db_session(self):
        async with self.__db_session() as session:
            yield session
