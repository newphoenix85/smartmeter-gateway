from app.models import UserLoginBase
from datetime import datetime
from pydantic import BaseModel

class IUserLoginUpdate(UserLoginBase):
    pass

class IUserLoginCreate(UserLoginBase):
    pass 

class IUserLogin(BaseModel):
    login: datetime