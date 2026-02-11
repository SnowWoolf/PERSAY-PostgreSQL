# app/db/session.py
from __future__ import annotations

from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.db.models import Base


_engine = None
_SessionLocal: Optional[sessionmaker] = None


# ─────────────────────────────────────────────────────────────
# INIT ENGINE (вызывается после load_yaml_config)
# ─────────────────────────────────────────────────────────────
def init_engine() -> None:
    global _engine, _SessionLocal

    if _engine is not None:
        return

    db_url = settings.db_url

    if db_url.startswith("sqlite"):
        raise RuntimeError("SQLite запрещён. Ожидается PostgreSQL.")

    _engine = create_engine(
        db_url,
        future=True,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

    _SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=_engine,
        future=True,
    )


# ─────────────────────────────────────────────────────────────
def init_db() -> None:
    if _engine is None:
        raise RuntimeError("Engine не инициализирован")
    Base.metadata.create_all(bind=_engine)


# ─────────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    if _SessionLocal is None:
        raise RuntimeError("SessionLocal не инициализирован")

    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()

