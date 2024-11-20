from pydantic import BaseModel, UUID4


class GroupBase(BaseModel):
    name: str


class CreateGroupBase(GroupBase):
    pass


class GroupBase(GroupBase):
    uuid: UUID4

    class Config:
        orm_mode = True
