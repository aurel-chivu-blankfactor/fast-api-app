from sqlalchemy.orm import Session
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate, Group as GroupSchema
from uuid import UUID


def create_group(db: Session, group: GroupCreate):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_group(db: Session, group_uuid: UUID):
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group is None:
        return None
    return GroupSchema(
        uuid=group.uuid, name=group.name, users=[user.name for user in group.users]
    )


def get_groups(db: Session):
    groups = db.query(Group).all()
    return [
        GroupSchema(
            uuid=group.uuid, name=group.name, users=[user.name for user in group.users]
        )
        for group in groups
    ]


def update_group(db: Session, group_uuid: UUID, updated_data: dict):
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group is None:
        return None
    for key, value in updated_data.items():
        if value is not None:
            setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return GroupSchema(
        uuid=group_uuid, name=group.name, users=[u.name for u in group.users]
    )


def delete_group(db: Session, group_uuid: UUID):
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group is None:
        return None
    db.delete(group)
    db.commit()
    return group
