"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
Database Layer - SQLite + SQLAlchemy
"""

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "german_ai.db")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SavedAnalysis(Base):
    __tablename__ = "saved_analyses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    level = Column(String(10), nullable=False)
    topic = Column(String(255), nullable=False)
    provider = Column(String(50), default="gemini")
    summary_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SavedConjugation(Base):
    __tablename__ = "saved_conjugations"

    id = Column(Integer, primary_key=True, index=True)
    verb = Column(String(100), unique=True, index=True, nullable=False)
    turkish_meaning = Column(String(255), nullable=False)
    is_regular = Column(Boolean, default=True)
    auxiliary_verb = Column(String(20), default="haben")
    conjugation_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class FavoriteWord(Base):
    __tablename__ = "favorite_words"

    id = Column(Integer, primary_key=True, index=True)
    german = Column(String(150), nullable=False)
    turkish = Column(String(150), nullable=False)
    article = Column(String(10), nullable=True)
    plural = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Veritabanı tablolarını oluşturur."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI için Veritabanı Session Dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully at:", DB_PATH)
