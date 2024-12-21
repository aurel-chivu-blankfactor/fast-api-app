import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.association_tables import user_group


class User(Base):
    __tablename__ = "user"

    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    urls = Column(JSON, default={})
    groups = relationship("Group", secondary=user_group, back_populates="users")
