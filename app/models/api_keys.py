from sqlalchemy import (
    Column,
    Integer,
    String,
)

from . import Base


class APIKeyModel(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String(255))
    status = Column(Integer, default=1, nullable=False)