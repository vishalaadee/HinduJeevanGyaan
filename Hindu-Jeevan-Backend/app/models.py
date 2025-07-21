from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum


class AppointmentType(str, enum.Enum):
    kundali = "kundali"
    pooja = "pooja"
    consultation = "consultation"


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # ✅ Required for login auth


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    pob = Column(String, nullable=False)
    tob = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    appointment_type = Column(SqlEnum(AppointmentType), nullable=False)
    request_date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(String)
    rating = Column(Integer, nullable=True)  # ✅ Add this line
    created_at = Column(DateTime, default=datetime.utcnow)
