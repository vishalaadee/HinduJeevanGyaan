from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback/")
def submit_feedback(data: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    return crud.create_feedback(db, data)
