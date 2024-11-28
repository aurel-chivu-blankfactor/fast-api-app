from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user import (
    create_user as create_user_service,
    get_user as get_user_service,
    get_users as get_users_service,
    update_user as update_user_service,
    delete_user as delete_user_service,
)

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/", response_model=User)
async def create_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = await create_user_service(db, user_data, background_tasks)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid group UUID")
    return user


@router.get("/{user_uuid}", response_model=User)
def read_user(user_uuid: UUID, db: Session = Depends(get_db)):
    user = get_user_service(db, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    return get_users_service(db)


@router.patch("/{user_uuid}", response_model=User)
def update_user(
    user_uuid: UUID, user_update: UserUpdate, db: Session = Depends(get_db)
):
    user = update_user_service(db, user_uuid, user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_uuid}", response_model=dict)
def delete_user(user_uuid: UUID, db: Session = Depends(get_db)):
    user = delete_user_service(db, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted successfully"}
