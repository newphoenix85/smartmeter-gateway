from datetime import datetime
from pydantic import BaseModel
from app.models.smartland_smgw_model import SmartlandSMGWBase

class ISmartlandSMGWUpdate(SmartlandSMGWBase):
    pass

class ISmartlandSMGWCreate(SmartlandSMGWBase):
    pass 

class ISmartlandSMGWRead(SmartlandSMGWBase):
    pass 

class ISmartlandSMGW(BaseModel):
    receive_ts: datetime