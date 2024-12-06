from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.database import initialize_db
from app.database.database_healt_check import check_db_health
from app.utils.custom_logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not check_db_health():
        logger.error("Database connection failed during startup")
        raise RuntimeError("Database connection failed during startup")
    initialize_db()
    logger.info("Application started successfully")
    yield
