from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


# ================== 疫苗记录 ==================
class VaccineRecordBase(BaseModel):
    name: str
    scheduled_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: Optional[str] = "pending"
    notes: Optional[str] = None
    age: Optional[str] = None
    module_id: str


class VaccineRecordCreate(VaccineRecordBase):
    pass


class VaccineRecordUpdate(BaseModel):
    name: Optional[str] = None
    scheduled_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    age: Optional[str] = None


class VaccineRecord(VaccineRecordBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ================== 健康档案 ==================
class HealthRecordBase(BaseModel):
    record_type: str
    title: str
    value: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None
    module_id: str


class HealthRecordCreate(HealthRecordBase):
    pass


class HealthRecordUpdate(BaseModel):
    record_type: Optional[str] = None
    title: Optional[str] = None
    value: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None


class HealthRecord(HealthRecordBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
