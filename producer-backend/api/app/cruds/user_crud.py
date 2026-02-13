from . import CRUDBase
from app.models import User
from app.schemas.user_schema import IUserCreate, IUserUpdate
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDUser(CRUDBase[User, IUserCreate, IUserUpdate]):

    async def create(self, *, obj_in: IUserCreate, db_session: AsyncSession | None = None) -> User:
        db_session = db_session or super().get_db().session
        db_obj = User.model_validate(obj_in)
        db_user = await super().get(id=db_obj.id)

        if db_user:
            return db_user
        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj
    
    async def get_by_id(self, *, id: str, db_session: AsyncSession | None = None) -> User | None:
        db_session = db_session or super().get_db().session
        return await super().get(id=id)

user_crud = CRUDUser(User)