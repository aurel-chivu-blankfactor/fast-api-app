from typing import AsyncContextManager

from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.database.database import Base, engine
from app.api.v1.routers.root import router as root_router
from app.api.v1.routers.group import router as group_router
from app.api.v1.routers.user import router as user_router
from app.database.database_healt_check import check_db_health
from app.exceptions.GroupNotFoundException import GroupNotFoundException
from app.exceptions.UserNotFoundException import UserNotFoundException
from app.utils.custom_logger import logger

Base.metadata.create_all(bind=engine)


async def lifespan(app: FastAPI) -> AsyncContextManager:
    if not check_db_health():
        logger.error("Database connection failed during startup")
        raise RuntimeError("Database connection failed during startup")
    logger.info("Application started successfully")
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404, content={"error": "User not found", "message": exc.message}
    )

@app.exception_handler(GroupNotFoundException)
async def group_not_found_exception_handler(request, exc: GroupNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": "Group not found", "message": exc.message},
    )


app.include_router(root_router)
app.include_router(user_router)
app.include_router(group_router)
