from sqlalchemy.orm import Session
from app.repository.group import (
    create_group as create_group_repo,
    get_group as get_group_repo,
    get_groups as get_groups_repo,
    update_group as update_group_repo,
    delete_group as delete_group_repo,
)
from app.schemas.group import Group, GroupCreate, GroupUpdate
from uuid import UUID


def create_group(db: Session, group_data: GroupCreate):
    group = create_group_repo(db, group_data)
    return Group(
        uuid=group.uuid, name=group.name, users=[user.name for user in group.users]
    )


def get_group(db: Session, group_uuid: UUID):
    group = get_group_repo(db, group_uuid)
    if group is None:
        return None
    return Group(
        uuid=group.uuid, name=group.name, users=[user.name for user in group.users]
    )


def get_groups(db: Session):
    groups = get_groups_repo(db)
    return [
        Group(
            uuid=group.uuid, name=group.name, users=[user.name for user in group.users]
        )
        for group in groups
    ]


def update_group(db: Session, group_uuid: UUID, group_update: GroupUpdate):
    group = update_group_repo(
        db, group_uuid, group_update.model_dump(exclude_unset=True)
    )
    if group is None:
        return None
    return Group(
        uuid=group_uuid, name=group.name, users=[user.name for user in group.users]
    )


def delete_group(db: Session, group_uuid: UUID):
    group = delete_group_repo(db, group_uuid)
    if group is None:
        return None
    return Group(
        uuid=group.uuid, name=group.name, users=[user.name for user in group.users]
    )
