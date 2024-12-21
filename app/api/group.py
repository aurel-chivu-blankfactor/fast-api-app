from uuid import UUID
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.exceptions.exceptions import GroupNotFoundException
from app.schemas.group import Group, GroupCreate, GroupUpdate
from app.services.group import (
    create_group as create_group_service,
    get_group as get_group_service,
    get_groups as get_groups_service,
    update_group as update_group_service,
    delete_group as delete_group_service,
)

router = APIRouter(prefix="/group", tags=["groups"])


@router.post("/", response_model=Group)
def create_group(group: GroupCreate, db: Session = Depends(get_db)) -> Group:
    return create_group_service(db, group)


@router.get("/{group_uuid}", response_model=Group)
def read_group(group_uuid: UUID, db: Session = Depends(get_db)) -> Group | JSONResponse:
    try:
        return get_group_service(db, group_uuid)
    except GroupNotFoundException as exc:
        return JSONResponse(
            status_code=404,
            content={"error": "Group not found", "message": exc.message},
        )


@router.get("/", response_model=list[Group])
def read_groups(db: Session = Depends(get_db)) -> list[Group]:
    return get_groups_service(db)


@router.patch("/{group_uuid}", response_model=Group)
def update_group(
    group_uuid: UUID, group_update: GroupUpdate, db: Session = Depends(get_db)
) -> Group | JSONResponse:
    try:
        return update_group_service(db, group_uuid, group_update)
    except GroupNotFoundException as exc:
        return JSONResponse(
            status_code=404,
            content={"error": "Group not found", "message": exc.message},
        )


@router.delete("/{group_uuid}", response_model=dict)
def delete_group(
    group_uuid: UUID, db: Session = Depends(get_db)
) -> dict | JSONResponse:
    try:
        delete_group_service(db, group_uuid)
        return {
            "status": f"Group with the id {str(group_uuid)} was deleted successfully"
        }
    except GroupNotFoundException as exc:
        return JSONResponse(
            status_code=404,
            content={"error": "Group not found", "message": exc.message},
        )
