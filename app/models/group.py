import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.association_tables import user_group


class Group(Base):
    __tablename__ = "group"

    uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    users = relationship("User", secondary=user_group, back_populates="groups")
