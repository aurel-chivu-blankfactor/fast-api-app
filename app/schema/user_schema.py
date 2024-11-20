from pydantic import BaseModel, UUID4
from typing import List, Optional


class BaseUser(BaseModel):
    name: str
    urls: Optional[List[str]]


class UserCreate(BaseUser):
    group_uuid: UUID4


class User(BaseUser):
    uuid: UUID4
    group_name: str

    class Config:
        orm_mode = True
