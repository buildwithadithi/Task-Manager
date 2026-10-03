from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.database import get_db
from app.services import task_service
from app.dependencies import get_current_user

router = APIRouter()


@router.get(
    "/tasks",
    response_model=list[TaskResponse]
)
async def get_tasks(
    current_user: User = Depends(get_current_user),
    completed: bool | None = None,
    title: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await task_service.get_tasks(
        db,
        current_user.id,
        completed,
        title,
    )


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.get_task(
        db,
        task_id,
        current_user.id,
    )


@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.create_task(
        db,
        task,
        current_user.id,
    )


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
async def update_task(
    task_id: int,
    updated_task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.update_task(
        db,
        task_id,
        updated_task,
        current_user.id,
    )


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
async def patch_task(
    task_id: int,
    updated_task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await task_service.patch_task(
        db,
        task_id,
        updated_task,
        current_user.id,
    )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await task_service.delete_task(
        db,
        task_id,
        current_user.id,
    )