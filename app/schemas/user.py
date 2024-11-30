from pydantic import BaseModel, UUID4
from typing import List, Optional, Union


class UserBase(BaseModel):
    name: str
    urls: Optional[Union[dict, list]] = {}


class UserCreate(UserBase):
    group_uuid: UUID4


class User(UserBase):
    uuid: UUID4
    groups: List[str]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    urls: Optional[Union[dict, list]] = {}
    groups: Optional[List[str]] = None

    class Config:
        orm_mode: True
