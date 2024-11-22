from pydantic import BaseModel, UUID4
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    urls: Optional[List[str]] = []


class UserCreate(UserBase):
    group_uuid: UUID4


class User(UserBase):
    uuid: UUID4
    groups: List[str]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    urls: Optional[List[str]] = None
    groups: Optional[List[str]] = None

    class Config:
        orm_mode: True
