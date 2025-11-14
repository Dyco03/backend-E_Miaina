from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# 
load_dotenv()



try:
    DATABASE_URL = 'test'
    # DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/threedwear"

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in environment variables.")
except Exception as e:
    raise RuntimeError("Failed to load database configuration value is",DATABASE_URL) from e

# Création du moteur SQLAlchemy
engine = create_engine('mysql+pymysql://mit:123456@localhost:3306/eaina')

# Session locale pour les transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modèles
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()