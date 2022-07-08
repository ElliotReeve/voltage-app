from pydantic import BaseModel


class APIKeysDTO(BaseModel):
    id: int
    api_key: str
    linked: int
    status: int

    class Config(object):
        orm_mode = True

class APIKeysCreateDTO(BaseModel):
    api_key: str
