import os
os.environ["PGCLIENTENCODING"] = "utf-8"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

print("🧩 DATABASE_URL loaded:", repr(settings.DATABASE_URL))  # <-- agrega esto

engine = create_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for getting database sesion"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
