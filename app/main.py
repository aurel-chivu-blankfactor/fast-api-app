from fastapi import FastAPI
from app.database.database import initialize_db
from app.api.group import router as group_router
from app.api.user import router as user_router
from app.database.database_healt_check import check_db_health
from app.exceptions.group_not_found_exception import GroupNotFoundException
from app.exceptions.user_not_found_exception import UserNotFoundException
from app.exceptions.exception_handlers import (
    user_not_found_exception_handler,
    group_not_found_exception_handler,
)
from app.services.startup import lifespan

initialize_db()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {
        "message": "Welcome to the user and group management API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/healthcheck")
def healthcheck():
    db_health = check_db_health()
    if db_health:
        return {"status": "healthy"}
    return {"status": "unhealthy"}


app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(GroupNotFoundException, group_not_found_exception_handler)

app.include_router(user_router)
app.include_router(group_router)
