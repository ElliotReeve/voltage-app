from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VoltagesDTO(BaseModel):
    id: int
    main_battery: float
    auxiliary_battery: Optional[float] = None
    date: datetime

    class Config(object):
        orm_mode = True

class VoltagesCreateDTO(BaseModel):
    main_battery: float
    auxiliary_battery: Optional[float] = None
    api_key: Optional[str]