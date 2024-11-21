from pydantic import BaseModel, UUID4
from typing import List


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    uuid: UUID4
    users: List[str]

    class Config:
        orm_mode = True
