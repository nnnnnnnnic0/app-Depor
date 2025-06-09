# app/database.py

from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Ahora usamos la URL completa en settings.DATABASE_URL
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    # Crea las tablas según los modelos SQLModel registrados
    SQLModel.metadata.create_all(bind=engine)
