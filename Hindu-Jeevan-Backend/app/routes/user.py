# app/routes/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/appointment/", response_model=schemas.AppointmentResponse)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = models.Appointment(**appointment.dict())
    db_appointment.request_date = datetime.utcnow()
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
