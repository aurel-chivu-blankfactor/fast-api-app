from sqlalchemy.orm import Session
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate
from uuid import UUID


def create_group(db: Session, group: GroupCreate):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_group(db: Session, group_uuid: UUID):
    return db.query(Group).filter(Group.uuid == str(group_uuid)).first()


def get_groups(db: Session):
    return db.query(Group).all()


def update_group(db: Session, group_uuid: UUID, updated_data: dict):
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group:
        for key, value in updated_data.items():
            if value is not None:
                setattr(group, key, value)
        db.commit()
        db.refresh(group)
    return group


def delete_group(db: Session, group_uuid: UUID):
    group = db.query(Group).filter(Group.uuid == str(group_uuid)).first()
    if group:
        db.delete(group)
        db.commit()
    return group
