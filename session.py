from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.models import Base


# ─────────────────────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────────────────────
engine = create_engine(
    settings.db_url,               # postgresql+psycopg2://...
    future=True,
    pool_pre_ping=True,            # убирает зависшие коннекты
    pool_size=10,
    max_overflow=20,
)


# ─────────────────────────────────────────────────────────────
# SESSION FACTORY
# ─────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


# ─────────────────────────────────────────────────────────────
# INIT DB
# вызывается из main.py на startup
# ─────────────────────────────────────────────────────────────
def init_db() -> None:
    Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────────────────────
# DEPENDENCY
# ─────────────────────────────────────────────────────────────
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
