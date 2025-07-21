from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud, auth
from app.database import get_db

router = APIRouter()


@router.post("/admin/create")
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    existing = crud.get_admin_by_email(db, admin.email)
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    db_admin = crud.create_admin(db, admin)
    return {"message": "Admin created successfully", "admin_id": db_admin.id}


@router.post("/admin/login")
def admin_login(data: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = crud.get_admin_by_email(db, data.email)
    if not admin or not auth.verify_password(data.password, admin.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": admin.email})
    return {"access_token": token, "token_type": "bearer"}
