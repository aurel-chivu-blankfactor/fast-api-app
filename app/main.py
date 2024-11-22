from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.v1.routers.group import router as group_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


# @app.get("/health-check")
# def health_check(db: Session = Depends(get_db)):
#     try:
#         db.execute(text("SELECT 1"))
#         return {"status": "Database connection is healthy!"}
#     except Exception as e:
#         return {"status": "Database connection failed!", "error": str(e)}

# app.include_router(user)
app.include_router(group_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the user and group management API",
        "docs": "/docs",
        "redoc": "/redoc",
    }
