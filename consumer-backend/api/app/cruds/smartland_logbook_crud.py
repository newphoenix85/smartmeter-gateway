from typing import List

from sqlalchemy import Select
from . import CRUDBase
from app.models.logbook_model import SmartlandLogbook
from app.schemas.smartland_logbook_schema import ILogbookCreate, ILogbookUpdate
from sqlmodel.ext.asyncio.session import AsyncSession



class CRUDSmartlandLogbook(CRUDBase[SmartlandLogbook, ILogbookCreate, ILogbookUpdate]):

    async def create(self, *, obj_in: ILogbookCreate, db_session: AsyncSession | None = None) -> SmartlandLogbook:
        db_session = db_session or super().get_db().session
        db_obj = SmartlandLogbook.model_validate(obj_in)
        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj
    
    async def read_by_type(self, *, type: str, db_session: AsyncSession | None = None) ->  List[SmartlandLogbook]:
        db_session = db_session or super().get_db().session
        query = Select(self.model).where(self.model.type == type)
        response = await db_session.execute(query)
        rows = response.scalars().all()
        return rows
    


smartland_logbook_crud = CRUDSmartlandLogbook(SmartlandLogbook)