from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VoltagesDTO(BaseModel):
    id: int
    voltage: float
    date: datetime

    class Config(object):
        orm_mode = True

class VoltagesCreateDTO(BaseModel):
    voltage: float
    api_key: Optional[str]