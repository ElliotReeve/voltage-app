from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .api_keys import APIKeyModel
from .voltages import VoltagesModel