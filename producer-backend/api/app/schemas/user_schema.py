from app.models import UserBase
from app.schemas.user_login_schema import IUserLogin
from typing import List, Optional



class IUserCreate(UserBase):
    pass 

class IUserUpdate(UserBase):
    pass 

class IUserProfile(UserBase):
    logins: Optional[List[IUserLogin]]