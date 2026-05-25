from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os

Base = declarative_base()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_SQLITE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database.db')}"

DATABASE_URL = os.environ.get("DATABASE_URL", _SQLITE_URL)

# Supabase and older Postgres providers return postgres://, SQLAlchemy 2.x requires postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    Base.metadata.create_all(engine)
