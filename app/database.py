from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

pool_recycle = 3600
engine = create_engine(settings.database_url, pool_recycle=pool_recycle, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()