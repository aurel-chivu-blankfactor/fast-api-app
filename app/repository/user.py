from typing import Optional, List
from sqlalchemy.orm import Session
from app.exceptions.exceptions import UserNotFoundException, GroupNotFoundException
from app.models.user import User
from app.models.group import Group
from app.schemas.user import UserCreate
from uuid import UUID


def create_user(db: Session, user: UserCreate) -> User:
    group = db.query(Group).filter(Group.uuid == str(user.group_uuid)).first()

    if group is None:
        raise GroupNotFoundException(user.group_uuid)
    new_user = User(name=user.name, urls=user.urls)
    new_user.groups.append(group)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user_urls(db: Session, user_uuid: UUID, urls: dict) -> User:
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is not None:
        user.urls = urls
        db.commit()
        db.refresh(user)
    return user


def get_user(db: Session, user_uuid: UUID) -> Optional[User]:
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        raise UserNotFoundException(str(user_uuid))
    return user


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def update_user(db: Session, user_uuid: UUID, updated_data: dict) -> User:
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        raise UserNotFoundException(str(user_uuid))

    if "groups" in updated_data:
        group_names = updated_data.pop("groups")
        groups = db.query(Group).filter(Group.name.in_(group_names)).all()
        if len(groups) != len(group_names):
            raise GroupNotFoundException(
                None, "One or more groups not found in the database"
            )
        user.groups = groups

    for key, value in updated_data.items():
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_uuid: UUID) -> User:
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        raise UserNotFoundException(str(user_uuid))
    db.delete(user)
    db.commit()
    return user
