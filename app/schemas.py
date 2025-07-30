from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: datetime

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[datetime] = None

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ActivityLogBase(BaseModel):
    action: str
    endpoint: str
    method: str
    details: Optional[str] = None

class ActivityLogCreate(ActivityLogBase):
    order_id: Optional[int] = None

class ActivityLog(ActivityLogBase):
    id: int
    order_id: Optional[int]
    timestamp: datetime
    
    class Config:
        orm_mode = True

class PatientInfo(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime 