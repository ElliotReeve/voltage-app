from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
)

from . import Base


class VoltagesModel(Base):
    __tablename__ = "voltage_readings"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(Integer, nullable=False)
    main_battery = Column(Float, nullable=False)
    auxiliary_battery = Column(Float, nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.now())