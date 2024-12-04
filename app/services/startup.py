from typing import AsyncContextManager
from fastapi import FastAPI
from app.database.database_healt_check import check_db_health
from app.utils.custom_logger import logger


async def lifespan(app: FastAPI) -> AsyncContextManager:
    if not check_db_health():
        logger.error("Database connection failed during startup")
        raise RuntimeError("Database connection failed during startup")
    logger.info("Application started successfully")
    yield
