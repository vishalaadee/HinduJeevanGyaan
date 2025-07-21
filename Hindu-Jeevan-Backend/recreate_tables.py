# recreate_tables.py
from app.models import Base
from app.database import engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
