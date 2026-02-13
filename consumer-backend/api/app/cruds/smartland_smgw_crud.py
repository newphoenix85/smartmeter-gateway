from typing import List
from pydantic import TypeAdapter
from sqlalchemy import Select
from . import CRUDBase
from app.models.smartland_smgw_model import SmartlandSMGW
from app.schemas.smartland_smgw_schema import ISmartlandSMGWCreate, ISmartlandSMGWUpdate, ISmartlandSMGWRead
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDSmartlandSMGW(CRUDBase[SmartlandSMGW, ISmartlandSMGWCreate, ISmartlandSMGWUpdate]):

    async def create(self, *, obj_in: ISmartlandSMGWCreate, db_session: AsyncSession | None = None) -> SmartlandSMGW:
        db_session = db_session or super().get_db().session
        db_obj = SmartlandSMGW.model_validate(obj_in)
        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj
    
    async def read(self, *, obj_in: str, db_session: AsyncSession | None = None) ->  List[SmartlandSMGW]:
        db_session = db_session or super().get_db().session
        query = Select(self.model).where(self.model.user_id == obj_in).order_by(self.model.ts.desc())
        response = await db_session.execute(query)
        rows = response.scalars().all()
        return rows
    
    async def readOne(self, *, obj_in: str, db_session: AsyncSession | None = None) ->  SmartlandSMGW:
        db_session = db_session or super().get_db().session
        query = Select(self.model).where(self.model.user_id == obj_in).order_by(self.model.ts.desc())
        response = await db_session.execute(query)
        db_smgw_rows = response.scalars().first()
        return db_smgw_rows


smartland_smgw_crud = CRUDSmartlandSMGW(SmartlandSMGW)