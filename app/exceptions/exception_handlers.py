from fastapi.responses import JSONResponse
from fastapi import Request
from app.exceptions.group_not_found_exception import GroupNotFoundException
from app.exceptions.user_not_found_exception import UserNotFoundException


async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=404, content={"error": "User not found", "message": exc.message}
    )


async def group_not_found_exception_handler(
    request: Request, exc: GroupNotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": "Group not found", "message": exc.message},
    )
