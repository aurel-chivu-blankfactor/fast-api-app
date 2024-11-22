from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.repository.user import (
    create_user as create_user_repo,
    get_users,
    get_user,
    update_user as update_user_repo,
    delete_user as delete_user_repo,
)

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user_repo(db, user)
    print(user)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid group UUID")
    return user


@router.get("/{user_uuid}", response_model=User)
def read_user(user_uuid: UUID, db: Session = Depends(get_db)):
    user = get_user(db, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.patch("/{user_uuid}", response_model=User)
def update_user(
    user_uuid: UUID, user_update: UserUpdate, db: Session = Depends(get_db)
):
    updated_data = user_update.model_dump(exclude_unset=True)
    user = update_user_repo(db, user_uuid, updated_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_uuid}", response_model=dict)
def delete_user(user_uuid: UUID, db: Session = Depends(get_db)):
    user = delete_user_repo(db, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted successfully"}
