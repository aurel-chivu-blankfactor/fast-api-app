from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.schemas.group import Group, GroupCreate, GroupUpdate
from app.repository.group import (
    create_group as create_group_repo,
    get_group,
    get_groups,
    update_group as update_group_repo,
    delete_group as delete_group_repo,
)

router = APIRouter(prefix="/group", tags=["groups"])


@router.post("/", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    return create_group_repo(db, group)


@router.get("/{group_uuid}", response_model=Group)
def read_group(group_uuid: UUID, db: Session = Depends(get_db)):
    group = get_group(db, group_uuid)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.get("/", response_model=list[Group])
def read_groups(db: Session = Depends(get_db)):
    return get_groups(db)


@router.patch("/{group_uuid}", response_model=Group)
def update_group(
    group_uuid: UUID, group_update: GroupUpdate, db: Session = Depends(get_db)
):
    updated_data = group_update.model_dump(exclude_unset=True)
    group = update_group_repo(db, group_uuid, updated_data)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.delete("/{group_uuid}", response_model=dict)
def delete_group(group_uuid: UUID, db: Session = Depends(get_db)):
    group = delete_group_repo(db, group_uuid)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"status": "Group deleted successfully"}
