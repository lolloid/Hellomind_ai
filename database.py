"""
HelloMind — Database Setup (SQLAlchemy + SQLite)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Gunakan database MySQL dari XAMPP: user 'root', tanpa password, database 'hellomind'
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/hellomind")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True,  # Prevent MySQL server has gone away errors
    pool_recycle=3600,   # Recycle connections after an hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables if they don't exist."""
    from models import User, Chat, Message, MoodEntry  # noqa: F401
    Base.metadata.create_all(bind=engine)
