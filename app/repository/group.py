from typing import Optional

from sqlalchemy.orm import Session
from app.exceptions.exceptions import GroupNotFoundException
from app.models.group import Group
from app.schemas.group import GroupCreate
from uuid import UUID


def create_group(db: Session, group: GroupCreate) -> Group:
    new_group = Group(name=group.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def get_group(db: Session, group_uuid: UUID) -> Optional[Group]:
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group is None:
        raise GroupNotFoundException(str(group_uuid))
    return group


def get_groups(db: Session) -> list[Group]:
    return db.query(Group).all()


def update_group(db: Session, group_uuid: UUID, updated_data: dict) -> Group:
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group is None:
        raise GroupNotFoundException(str(group_uuid))
    for key, value in updated_data.items():
        if value is not None:
            setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group_uuid: UUID) -> Group:
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group is None:
        raise GroupNotFoundException(str(group_uuid))
    db.delete(group)
    db.commit()
    return group
