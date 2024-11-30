from fastapi import FastAPI

from app.core.database import Base, engine, get_db
from app.api.v1.routers.group import router as group_router
from app.api.v1.routers.user import router as user_router
from app.utils.database_healt_check import check_db_health
from app.utils.custom_logger import logger

Base.metadata.create_all(bind=engine)


async def lifespan(app):
    if not check_db_health():
        logger.error("Database connection failed during startup")
        raise RuntimeError("Database connection failed during startup")
    logger.info("Application started successfully")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(group_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the user and group management API",
        "docs": "/docs",
        "redoc": "/redoc",
    }
