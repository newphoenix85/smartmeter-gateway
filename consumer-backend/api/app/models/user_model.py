
from typing import TYPE_CHECKING
from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.ext.asyncio import AsyncAttrs

if TYPE_CHECKING:
    from app.models.user_login_model import UserLogin


class UserBase(AsyncAttrs, SQLModel):
    id: str = Field(
        schema_extra={"validation_alias": "sub"},
        default=None,
        primary_key=True
    )
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
    groups: list

class User(UserBase, table=True):
    __tablename__ = "tb_user"
    meter_id: int | None = Field(default=None)
    logins: list["UserLogin"] = Relationship(
        back_populates="user"
    )