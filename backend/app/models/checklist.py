from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModuleBase(BaseModel):
    name: str
    icon: Optional[str] = "📦"
    description: Optional[str] = None
    sort_order: Optional[int] = 0
    module_type: Optional[str] = "custom"  # custom, checklist, vaccine, health


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None


class Module(ModuleBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ItemCategoryBase(BaseModel):
    name: str
    module_id: str
    sort_order: Optional[int] = 0


class ItemCategoryCreate(ItemCategoryBase):
    pass


class ItemCategoryUpdate(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None


class ItemCategory(ItemCategoryBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChecklistItemBase(BaseModel):
    name: str
    module_id: str
    category_id: Optional[str] = None
    status: Optional[str] = "pending"
    link: Optional[str] = None
    notes: Optional[str] = None
    quantity: Optional[int] = 1
    sort_order: Optional[int] = 0


class ChecklistItemCreate(ChecklistItemBase):
    pass


class ChecklistItemUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[str] = None
    status: Optional[str] = None
    link: Optional[str] = None
    notes: Optional[str] = None
    quantity: Optional[int] = None
    sort_order: Optional[int] = None


class ChecklistItem(ChecklistItemBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
