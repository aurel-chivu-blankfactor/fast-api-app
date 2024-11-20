from pydantic import BaseModel, UUID4


class BaseGroup(BaseModel):
    name: str


class CreateGroup(BaseGroup):
    pass


class Group(BaseGroup):
    uuid: UUID4

    class Config:
        orm_mode = True
