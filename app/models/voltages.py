from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)

from . import Base


class VoltagesModel(Base):
    __tablename__ = "voltage_readings"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(Integer, nullable=False)
    voltage = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now())