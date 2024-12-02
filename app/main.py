from fastapi import FastAPI
from app.database.database import initialize_db
from app.api.v1.routers.root import router as root_router
from app.api.v1.routers.group import router as group_router
from app.api.v1.routers.user import router as user_router
from app.exceptions.GroupNotFoundException import GroupNotFoundException
from app.exceptions.UserNotFoundException import UserNotFoundException
from app.utils.exception_handlers import (
    user_not_found_exception_handler,
    group_not_found_exception_handler,
)
from app.utils.lifespan import lifespan

initialize_db()

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(GroupNotFoundException, group_not_found_exception_handler)

app.include_router(root_router)
app.include_router(user_router)
app.include_router(group_router)
