# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

DATABASE_URL = "postgresql://hindu_admin:Vishal%40123@localhost/hindu_jeevan_gyaan_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ✅ This is the missing function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
