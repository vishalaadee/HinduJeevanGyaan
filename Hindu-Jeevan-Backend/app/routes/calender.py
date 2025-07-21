# app/routes/calendar.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime, timedelta

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.get("/appointments/upcoming")
def get_upcoming_appointments(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    upcoming = db.query(models.Appointment).filter(models.Appointment.request_date > now).all()
    return upcoming

# Google Calendar integration will go here in the future
