from sqlalchemy import String
from sqlmodel import Field, SQLModel, Column 
from enum import Enum

class TypeEnum(str, Enum):
    SYS = 'SYS'
    CAL = 'CAL'
    USER = 'USER'

class LevelEnum(str, Enum):
    I = 'I'
    W = 'W'
    E = 'E'
    F = 'F'

class SmartlandLogbookBase(SQLModel):
    id: str = Field(primary_key=True)
    user_id: str | None = Field(default=None, index=True, foreign_key="tb_user.id")
    type: TypeEnum | None = Field(
        sa_column=Column(
            String(),
            nullable=False
        )
    )
    event: str | None = Field(
        sa_column=Column(
            String(),
            nullable=False
        )
    )
    level: LevelEnum | None = Field(
        sa_column=Column(
            String(),
            nullable=False
        )
    )
    checked: bool | None = Field(default=None)

    

class SmartlandLogbook(SmartlandLogbookBase, table=True):
    __tablename__ = "tb_logbook"