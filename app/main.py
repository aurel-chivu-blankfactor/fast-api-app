from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.core.database import get_db

app = FastAPI()

@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database connection is healthy!"}
    except Exception as e:
        return {"status": "Database connection failed!", "error": str(e)}
