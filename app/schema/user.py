from pydantic import BaseModel, UUID4
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    urls: Optional[List[str]]


class UserBaseCreate(UserBase):
    group_uuid: UUID4


class UserBase(UserBase):
    uuid: UUID4
    group_name: str

    class Config:
        orm_mode = True
