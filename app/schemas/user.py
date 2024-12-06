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

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: Optional[str] = None
    urls: Optional[Union[dict, list]] = {}
    groups: Optional[List[str]] = None

    model_config = {"from_attributes": True}
