from typing import  Union
from sqlmodel import SQLModel
from . import UserOidc



class OIDCToken(SQLModel):
    access_token: str
    token_type: str
    expires_in: int
    id_token: str
    refresh_token: str
    expires_at: int
    user_info: Union[UserOidc]