# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routes import (
    user,
    appointment,
    admin,
    feedback,
    calender,
    analytics
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hindu Jeevan Gyaan Backend",
    description="API backend for appointment booking, astrology consultation, and admin analytics",
    version="1.0.0"
)

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(user.router)
app.include_router(appointment.router)
app.include_router(admin.router)
app.include_router(feedback.router)
app.include_router(calender.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Hindu Jeevan Gyaan API"}
