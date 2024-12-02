from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to the user and group management API",
        "docs": "/docs",
        "redoc": "/redoc",
    }
