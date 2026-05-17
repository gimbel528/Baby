from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LetterBase(BaseModel):
    title: str
    content: str
    unlock_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None


class LetterCreate(LetterBase):
    pass


class LetterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    unlock_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    is_unlocked: Optional[bool] = None


class Letter(LetterBase):
    id: str
    user_id: str
    is_unlocked: bool
    is_reminded: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
