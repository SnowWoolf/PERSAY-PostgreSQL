from __future__ import annotations

from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.models import Base


def _ensure_sqlite_dir(db_url: str) -> None:
    if db_url.startswith("sqlite"):
        prefix = "sqlite:///"
        if db_url.startswith(prefix):
            fs_path = db_url[len(prefix):]

            if fs_path == ":memory:":
                return

            d = Path(fs_path).resolve().parent
            d.mkdir(parents=True, exist_ok=True)


db_url = settings.db_url
_ensure_sqlite_dir(db_url)

engine = create_engine(
    db_url,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
