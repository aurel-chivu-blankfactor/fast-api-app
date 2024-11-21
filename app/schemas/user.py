from pydantic import BaseModel, UUID4
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    urls: Optional[List[str]] = []


class UserCreate(UserBase):
    group_uuid: UUID4


class User(UserBase):
    uuid: UUID4
    group_name: str

    class Config:
        orm_mode = True
