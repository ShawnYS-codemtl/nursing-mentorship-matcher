from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
import os

Base = declarative_base()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "database.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

def init_db():
    Base.metadata.create_all(engine)