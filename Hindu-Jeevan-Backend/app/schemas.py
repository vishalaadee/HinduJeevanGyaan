from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import AppointmentType


class AdminCreate(BaseModel):
    email: EmailStr
    password: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class AppointmentCreate(BaseModel):
    name: str
    dob: str
    pob: str
    tob: str
    gender: str
    appointment_type: AppointmentType
    request_date: Optional[datetime] = None


class AppointmentResponse(AppointmentCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class FeedbackCreate(BaseModel):
    name: str
    content: str
    rating: Optional[int] = None  # ✅ Add this line

