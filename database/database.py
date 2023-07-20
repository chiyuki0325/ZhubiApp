from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 程序内模块
from settings import settings

Base = declarative_base()


class Database:
    def __init__(self):
        url: str = f'postgresql+asyncpg://{settings.postgresql_user}:{settings.postgresql_password}@' \
                   f'{settings.postgresql_host}:{settings.postgresql_port}/{settings.postgresql_database}'
        self.engine: AsyncEngine = create_async_engine(
            url,
            echo=settings.loglevel == 'DEBUG'
        )
        self.async_session: sessionmaker = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def create_columns(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
