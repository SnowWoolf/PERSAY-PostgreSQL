# app/db/session.py
# Для работы с SQLite и PostgreSQL (не протестирован!!)
from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.db.models import Base


# ─────────────────────────────────────────────
# ГЛОБАЛЬНЫЕ ОБЪЕКТЫ
# ─────────────────────────────────────────────
engine = None

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    future=True,
)


# ─────────────────────────────────────────────
# INIT ENGINE
# вызывается ТОЛЬКО после load_yaml_config()
# ─────────────────────────────────────────────
def init_engine() -> None:
    global engine

    db_url = settings.db_url

    if not db_url:
        raise RuntimeError("db.url not configured")

    # ───── SQLite ─────
    if db_url.startswith("sqlite"):
        engine = create_engine(
            db_url,
            future=True,
            connect_args={"check_same_thread": False},
        )

    # ───── PostgreSQL ─────
    elif db_url.startswith("postgresql"):
        engine = create_engine(
            db_url,
            future=True,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )

    else:
        raise RuntimeError(f"Unsupported DB: {db_url}")

    SessionLocal.configure(bind=engine)


# ─────────────────────────────────────────────
def init_db() -> None:
    if engine is None:
        raise RuntimeError("engine not initialized")
    Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
