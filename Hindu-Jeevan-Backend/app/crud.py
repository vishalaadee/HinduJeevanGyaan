from sqlalchemy.orm import Session
from app import models, schemas, auth


def create_admin(db: Session, admin: schemas.AdminCreate):
    hashed_pwd = auth.hash_password(admin.password)
    db_admin = models.Admin(email=admin.email, hashed_password=hashed_pwd)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()


def create_appointment(db: Session, appt: schemas.AppointmentCreate):
    db_appt = models.Appointment(**appt.dict())
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


def create_feedback(db: Session, fb: schemas.FeedbackCreate):
    db_fb = models.Feedback(**fb.dict())
    db.add(db_fb)
    db.commit()
    db.refresh(db_fb)
    return db_fb
