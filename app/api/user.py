from uuid import UUID
from fastapi import Depends, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.exceptions.exceptions import UserNotFoundException, GroupNotFoundException
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user import (
    create_user as create_user_service,
    get_user as get_user_service,
    get_users as get_users_service,
    update_user as update_user_service,
    delete_user as delete_user_service,
    update_user_urls_task,
)

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/", response_model=User)
async def create_user(
    user_data: UserCreate,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
) -> User:
    user = await create_user_service(db, user_data)
    background_task.add_task(update_user_urls_task, db, user.uuid)
    return user


@router.get("/{user_uuid}", response_model=User)
def read_user(user_uuid: UUID, db: Session = Depends(get_db)) -> User | JSONResponse:
    try:
        return get_user_service(db, user_uuid)
    except UserNotFoundException as exc:
        return JSONResponse(
            status_code=404, content={"error": "User not found", "message": exc.message}
        )


@router.get("/", response_model=list[User])
def read_users(db: Session = Depends(get_db)) -> list[User]:
    return get_users_service(db)


@router.patch("/{user_uuid}", response_model=User)
def update_user(
    user_uuid: UUID, user_update: UserUpdate, db: Session = Depends(get_db)
) -> User | JSONResponse:
    try:
        return update_user_service(db, user_uuid, user_update)
    except UserNotFoundException as exc:
        return JSONResponse(
            status_code=404, content={"error": "User not found", "message": exc.message}
        )
    except GroupNotFoundException as exc:
        return JSONResponse(
            status_code=404,
            content={"error": "Group not found", "message": exc.message},
        )


@router.delete("/{user_uuid}", response_model=dict)
def delete_user(user_uuid: UUID, db: Session = Depends(get_db)) -> dict | JSONResponse:
    try:
        delete_user_service(db, user_uuid)
        return {"status": f"User with the {str(user_uuid)} was deleted successfully"}
    except UserNotFoundException as exc:
        return JSONResponse(
            status_code=404, content={"error": "User not found", "message": exc.message}
        )
