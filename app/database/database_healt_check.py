from sqlalchemy import text
from app.database.database import get_engine_and_session
from app.utils.custom_logger import logger


def check_db_health() -> bool:
    logger.info("Starting database health check...")
    _, session_local = get_engine_and_session()
    try:
        db = session_local()
        db.execute(text("SELECT 1"))
        logger.info("Database connection is healthy!")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
    finally:
        db.close()
