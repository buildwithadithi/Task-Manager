from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    TaskNotFoundException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
)

async def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "TASK_NOT_FOUND",
            "message": "The requested task does not exist"
        }
    )
    
async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsException
):
    return JSONResponse(
        status_code=409,
        content={
            "error": "User_Already_Exists",
            "message": "The username already exists."
        }
    )
    
async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsException
):
    return JSONResponse(
        status_code=401,
        content={
            "error": "Invalid_Credentials",
            "message": "Invalid username or password."
        }
    )
    
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        }
    )
    
async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenException
):
    return JSONResponse(
        status_code=401,
        content={
            "error": "INVALID_TOKEN",
            "message": "Invalid or expired token."
        }
    )