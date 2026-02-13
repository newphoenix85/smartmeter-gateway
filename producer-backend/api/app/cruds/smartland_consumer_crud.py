from typing import List
from pydantic import TypeAdapter
from sqlalchemy import select
from . import CRUDBase
from app.models.smartland_smgw_model import SmartlandSMGW
from app.schemas.smartland_smgw_schema import ISmartlandSMGWCreate, ISmartlandSMGWUpdate, ISmartlandSMGWRead, ISmartlandSMGW
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDSmartlandConsumer(CRUDBase[ISmartlandSMGW, ISmartlandSMGWCreate, ISmartlandSMGWUpdate]):

    async def create(self, *, obj_in: ISmartlandSMGWCreate, db_session: AsyncSession | None = None) -> ISmartlandSMGW:
        db_session = db_session or super().get_db().session
        db_obj = SmartlandSMGW.model_validate(obj_in)
        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj
    
    async def read(self, *, obj_in: str, db_session: AsyncSession | None = None) ->  List[ISmartlandSMGW]:
        db_session = db_session or super().get_db().session
        db_consumer_rows = await super().getAllFromUser(id=obj_in)
        return db_consumer_rows

    async def read_all(self, db_session: AsyncSession | None = None) -> List[ISmartlandSMGW]:
        db_session = db_session or super().get_db().session
        query = select(SmartlandSMGW).order_by(SmartlandSMGW.receive_ts.desc())
        response = await db_session.execute(query)
        rows = response.scalars().all()
        return rows


smartland_consumer_crud = CRUDSmartlandConsumer(ISmartlandSMGW)