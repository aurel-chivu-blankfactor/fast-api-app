from sqlalchemy.orm import Session
from app.repository.user import (
    create_user as create_user_repo,
    get_user as get_user_repo,
    get_users as get_users_repo,
    update_user as update_user_repo,
    delete_user as delete_user_repo,
)
from app.schemas.user import User, UserCreate, UserUpdate
from uuid import UUID


def create_user(db: Session, user_data: UserCreate):
    user = create_user_repo(db, user_data)
    if user is None:
        return None
    return User(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[g.name for g in user.groups],
    )


def get_user(db: Session, user_uuid: UUID):
    user = get_user_repo(db, user_uuid)
    if user is None:
        return None
    return User(
        uuid=user.uuid, name=user.name, groups=[group.name for group in user.groups]
    )


def get_users(db: Session):
    users = get_users_repo(db)
    return [
        User(
            uuid=user.uuid,
            name=user.name,
            urls=user.urls,
            groups=[g.name for g in user.groups],
        )
        for user in users
    ]


def update_user(db: Session, user_uuid: UUID, user_update: UserUpdate):
    user = update_user_repo(db, user_uuid, user_update.model_dump(exclude_unset=True))
    if user is None:
        return None
    return User(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[g.name for g in user.groups],
    )


def delete_user(db: Session, user_uuid: UUID):
    user = delete_user_repo(db, user_uuid)
    if user is None:
        return None
    return User(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[group.name for group in user.groups],
    )
