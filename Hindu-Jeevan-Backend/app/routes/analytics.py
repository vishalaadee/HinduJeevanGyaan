# app/routes/analytics.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from sqlalchemy import func

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/appointments/count")
def appointment_count(db: Session = Depends(get_db)):
    count = db.query(func.count(models.Appointment.id)).scalar()
    return {"total_appointments": count}

@router.get("/feedback/average-rating")
def average_rating(db: Session = Depends(get_db)):
    avg_rating = db.query(func.avg(models.Feedback.rating)).scalar()
    return {"average_rating": round(avg_rating or 0, 2)}
