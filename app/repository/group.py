from sqlalchemy.orm import Session
from app.models.group import Group
from app.schemas.group import GroupCreate
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
