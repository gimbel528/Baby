from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CountdownEventBase(BaseModel):
    event_name: str
    target_date: datetime
    event_type: str = "custom"


class CountdownEventCreate(CountdownEventBase):
    pass


class CountdownEventUpdate(BaseModel):
    event_name: Optional[str] = None
    target_date: Optional[datetime] = None
    event_type: Optional[str] = None
    is_active: Optional[bool] = None


class CountdownEvent(CountdownEventBase):
    id: str
    user_id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
