from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import TaskNotFoundException, UserAlreadyExistsException, InvalidCredentialsException, InvalidTokenException
from app.exception_handler import task_not_found_handler, general_exception_handler, user_already_exists_handler, invalid_credentials_handler, invalid_token_handler
from app.routers.tasks import router as tasks_router
from app.config import settings
from app.routers.auth import router as auth_router
import time

app = FastAPI(
    title=settings.app_name,
    swagger_ui_parameters={
            "persistAuthorization": True
        },
    description="Backend API for managing tasks",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    print(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"→ {duration:.4f}s"
    )

    return response

@app.middleware("http")
async def add_app_header(request: Request, call_next):

    response = await call_next(request)

    response.headers["X-App-Name"] = "Task Manager"

    return response

app.include_router(tasks_router)
app.include_router(auth_router)

#FastAPI, when TaskNotFoundException occurs, use task_not_found_handler.
app.add_exception_handler(
    TaskNotFoundException,
    task_not_found_handler
)

app.add_exception_handler(
    UserAlreadyExistsException,
    user_already_exists_handler
)

app.add_exception_handler(
    InvalidCredentialsException,
    invalid_credentials_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)

app.add_exception_handler(
    InvalidTokenException,
    invalid_token_handler
)

