from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, DateTime

if TYPE_CHECKING:
    from app.models.user_model import User

class UserLoginBase(SQLModel):
    id: str = Field(primary_key=True)
    user_id: str | None = Field(default=None, index=True, foreign_key="tb_user.id")
    login_oidc: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )
    login: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=datetime.now
    )

class UserLogin(UserLoginBase, table=True):
    __tablename__ = "tb_login"
    user: Optional["User"] = Relationship(
        back_populates="logins"
    )