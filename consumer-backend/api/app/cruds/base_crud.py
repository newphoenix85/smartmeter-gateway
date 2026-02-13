from sqlmodel import SQLModel
from typing import List, TypeVar, Generic
from fastapi_async_sqlalchemy import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select
from pydantic import BaseModel
from uuid import UUID

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model
        self.db = db

    def get_db(self) -> type(db): # type: ignore
        return self.db
    
    async def get(self, *, id: UUID | str, db_session: AsyncSession | None = None) -> ModelType | None:
        db_session = db_session or self.db.session
        query = Select(self.model).where(self.model.id == id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()
    
    async def getAllFromUser(self, *, id: UUID | str, db_session: AsyncSession | None = None) -> List[ModelType] | None:
        db_session = db_session or self.db.session
        query = Select(self.model).where(self.model.user_id == id)
        response = await db_session.execute(query)
        rows = response.scalars().all()
        return rows
    
    