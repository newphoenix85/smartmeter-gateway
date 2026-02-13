import base64
import json
from jwt import encode, decode
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel
from dateutil.parser import isoparse
import datetime

secret = "zuEdpVpLht8zHQNMoyr7q4J2jyZmRBtuO0SU8uS9ju2mvzx5YuWSvDd4ZW45qjJS"
algo = "HS256"

class UserBase(SQLModel):
    sub: str = Field(index=True)
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)

class UserOidc(UserBase):
    auth_time: int
    iss: str
    aud: str
    exp: int
    iat: int
    acr: str
    email: str
    email_verified: bool
    name: str
    given_name: str
    preferred_username: str
    nickname: str
    groups: list[str]

@staticmethod
def parse_id_token(token: str) -> dict:


    return decode(token,
        secret,
        algorithms=[algo])

def create_token(
        sub: str,
        exp_in: int = 600, 
        name: str = "",
        given_name: str = "",
        preferred_username: str = "",
        email: str = "",
        nickname: str = "",
        groups: list[str] = [],
        auth_time: int = int(isoparse(datetime.datetime.now(datetime.timezone.utc).isoformat()).timestamp()),
        iat: int = int(isoparse(datetime.datetime.now(datetime.timezone.utc).isoformat()).timestamp()),
        iss: str = "",
        aud: str = "",
        acr: str = "") -> str:
    
    user_info = UserOidc(
        auth_time=auth_time,
        sub=sub,
        email=email,
        email_verified=True,
        name=name,
        given_name=given_name,
        preferred_username=preferred_username,
        nickname=nickname,
        groups=groups,
        iss=iss,
        aud=aud,
        exp=auth_time + exp_in,
        iat=iat,
        acr=acr,
    )

    user_info_token= encode(user_info.model_dump(), secret, algorithm=algo)
    return user_info_token
