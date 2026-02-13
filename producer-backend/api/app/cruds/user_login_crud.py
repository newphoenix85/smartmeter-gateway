from . import CRUDBase
from app.models.user_login_model import UserLogin
from app.schemas.user_login_schema import IUserLoginCreate, IUserLoginUpdate
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDUserLogin(CRUDBase[UserLogin, IUserLoginCreate, IUserLoginUpdate]):

    async def create(self, *, obj_in: IUserLoginCreate, db_session: AsyncSession | None = None) -> UserLogin:
        db_session = db_session or super().get_db().session
        db_obj = UserLogin.model_validate(obj_in)
        db_login = await super().get(id=db_obj.id)

        if db_login:
            return db_login
        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj
    
user_login_crud = CRUDUserLogin(UserLogin)