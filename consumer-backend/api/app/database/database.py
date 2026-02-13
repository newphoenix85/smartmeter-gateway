from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from collections.abc import AsyncGenerator
from app.internal.settings import DatabaseSettings

engine = create_async_engine(
    f"postgresql+asyncpg://{DatabaseSettings.sqlalchemy_database_server_user}:"
    f"{DatabaseSettings.sqlalchemy_database_server_password}@"
    f"{DatabaseSettings.sqlalchemy_database_server_name}:"
    f"{DatabaseSettings.sqlalchemy_database_server_port}/"
    f"{DatabaseSettings.sqlalchemy_database_server_database}", 
    connect_args={},
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine,
                            class_=AsyncSession,
                            expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session