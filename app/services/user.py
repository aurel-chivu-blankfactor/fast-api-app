from typing import Optional

from sqlalchemy.orm import Session
from app.repository.user import (
    create_user as create_user_repo,
    update_user_urls,
    get_user as get_user_repo,
    get_users as get_users_repo,
    update_user as update_user_repo,
    delete_user as delete_user_repo,
)
from app.schemas.user import User, UserCreate, UserUpdate
from uuid import UUID
import httpx


async def fetch_github_data(user_uuid: str) -> dict:
    github_api_url = "https://api.github.com/"
    async with httpx.AsyncClient() as client:
        response = await client.get(github_api_url)
        response.raise_for_status()
        data = response.json()
        transformed_data = {
            key: value.replace("{user}", user_uuid) if isinstance(value, str) else value
            for key, value in data.items()
        }
        return transformed_data


async def create_user(db: Session, user_data: UserCreate) -> User:
    user = create_user_repo(db, user_data)
    github_urls = await fetch_github_data(user.uuid)
    return User(
        uuid=user.uuid,
        name=user.name,
        urls=github_urls,
        groups=[g.name for g in user.groups],
    )


async def update_user_urls_task(db: Session, user_uuid: UUID) -> None:
    try:
        github_urls = await fetch_github_data(str(user_uuid))
        update_user_urls(db, user_uuid, github_urls)
    finally:
        db.close()


def get_user(db: Session, user_uuid: UUID) -> User:
    user = get_user_repo(db, user_uuid)
    return User(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[group.name for group in user.groups],
    )


def get_users(db: Session) -> list[User]:
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


def update_user(db: Session, user_uuid: UUID, user_update: UserUpdate) -> User:
    user = update_user_repo(db, user_uuid, user_update.model_dump(exclude_unset=True))
    return User(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[g.name for g in user.groups],
    )


def delete_user(db: Session, user_uuid: UUID) -> User:
    user = delete_user_repo(db, user_uuid)
    return User(
        uuid=user.uuid,
        name=user.name,
        urls=user.urls,
        groups=[group.name for group in user.groups],
    )
