from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os
from model import Base

_:bool = load_dotenv(find_dotenv())
DB_KEY = os.getenv('DB_KEY', "")

engine = create_engine(DB_KEY, echo=True)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()