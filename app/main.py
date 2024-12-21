from fastapi import FastAPI
from app.api.group import router as group_router
from app.api.user import router as user_router
from app.database.database_healt_check import check_db_health


from app.services.startup import lifespan

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


app.include_router(user_router)
app.include_router(group_router)
