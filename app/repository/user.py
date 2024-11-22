from sqlalchemy.orm import Session
from app.models.user import User
from app.models.group import Group
from app.schemas.user import UserCreate, User as UserSchema
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
    return UserSchema(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[g.name for g in user.groups],
    )


def get_user(db: Session, user_uuid: UUID):
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        return None
    return UserSchema(
        uuid=user.uuid, name=user.name, groups=[group.name for group in user.groups]
    )


def get_users(db: Session):
    users = db.query(User).all()
    return [
        UserSchema(
            uuid=user.uuid,
            name=user.name,
            urls=user.urls,
            groups=[g.name for g in user.groups],
        )
        for user in users
    ]


def update_user(db: Session, user_uuid: UUID, updated_data: dict):
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        return None
    for key, value in updated_data.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return UserSchema(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[g.name for g in user.groups],
    )


def delete_user(db: Session, user_uuid: UUID):
    user = db.query(User).filter(User.uuid == str(user_uuid)).first()
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return user
