from sqlalchemy.orm import Session
from app.models.user import User
from app.models.group import Group
from app.schemas.user import UserCreate
from uuid import UUID


def create_user(db: Session, user: UserCreate):
    group = db.query(Group).filter(Group.uuid == str(user.group_uuid)).first()
    if group is None:
        return None
    user = User(name=user.name, urls=user.urls)
    user.groups.append(group)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_urls(db: Session, user_uuid: UUID, urls: dict):
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is not None:
        user.urls = urls
        db.commit()
        db.refresh(user)
    return user


def get_user(db: Session, user_uuid: UUID):
    return db.query(User).filter(User.uuid == str(user_uuid)).first()


def get_users(db: Session):
    return db.query(User).all()


def update_user(db: Session, user_uuid: UUID, updated_data: dict):
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        return None
    for key, value in updated_data.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_uuid: UUID):
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return user
