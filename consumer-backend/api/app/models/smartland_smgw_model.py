from datetime import datetime
from sqlalchemy import BigInteger, String
from sqlmodel import Field, SQLModel, Column, DateTime



class SmartlandSMGWBase(SQLModel):
    id: str = Field(primary_key=True)
    user_id: str | None = Field(default=None, index=True, foreign_key="tb_user.id")
    ts: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )
    receive_ts: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        ),
        default_factory=datetime.now
    )
    meter_id: int = Field(
        sa_column=Column(
            BigInteger(),
            nullable=False
        )
    )
    value: int = Field(
        sa_column=Column(
            BigInteger(),
            nullable=False
        )
    )
    obis: str = Field(
        sa_column=Column(
            String(),
            nullable=False
        )
    )
    unit: str = Field(
        sa_column=Column(
            String(),
            nullable=False
        )
    )
    

class SmartlandSMGW(SmartlandSMGWBase, table=True):
    __tablename__ = "tb_smgw"