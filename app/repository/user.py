from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from uuid import UUID

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, urls=user.urls)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_uuid: UUID):
    return db.query(User).filter(User.uuid == str(user_uuid)).first()

def get_users(db: Session):
    return db.query(User).all()
