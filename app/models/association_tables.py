from sqlalchemy import Table, Column, ForeignKey, String
from app.database.database import Base

user_group = Table(
    "user_group",
    Base.metadata,
    Column(
        "user_uuid",
        String,
        ForeignKey("user.uuid"),
        primary_key=True,
    ),
    Column(
        "group_uuid",
        String,
        ForeignKey("group.uuid"),
        primary_key=True,
    ),
)
