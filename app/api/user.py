from uuid import UUID
from fastapi import Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.database import get_db
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
def read_user(user_uuid: UUID, db: Session = Depends(get_db)) -> User:
    return get_user_service(db, user_uuid)


@router.get("/", response_model=list[User])
def read_users(db: Session = Depends(get_db)) -> list[User]:
    return get_users_service(db)


@router.patch("/{user_uuid}", response_model=User)
def update_user(
    user_uuid: UUID, user_update: UserUpdate, db: Session = Depends(get_db)
) -> User:
    user = update_user_service(db, user_uuid, user_update)
    return user


@router.delete("/{user_uuid}", response_model=dict)
def delete_user(user_uuid: UUID, db: Session = Depends(get_db)) -> dict:
    delete_user_service(db, user_uuid)
    return {"status": f"User with the {str(user_uuid)} was deleted successfully"}
