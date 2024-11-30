from sqlalchemy import text
from app.database.database import SessionLocal
from app.utils.custom_logger import logger


def check_db_health():
    logger.info("Starting database health check...")
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        logger.info("Database connecton is healthy!")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
    finally:
        db.close()
