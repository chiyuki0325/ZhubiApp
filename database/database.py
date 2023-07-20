from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

# 程序内模块
from settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Database:
    def __init__(self):
        url: str = f'postgresql+asyncpg://{settings.postgresql_user}:{settings.postgresql_password}@' \
                   f'{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database}'
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=settings.loglevel == 'DEBUG'
        )
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    async def create_columns(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
