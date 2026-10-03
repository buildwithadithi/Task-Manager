from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import TaskCreate, TaskUpdate
from app.exceptions import TaskNotFoundException
from app.repositories import task_repository


async def get_tasks(
    db: AsyncSession,
    user_id: int,
    completed: bool | None = None,
    title: str | None = None,
):
    return await task_repository.get_tasks(
        db,
        user_id,
        completed,
        title,
    )


async def get_task(
    db: AsyncSession,
    task_id: int,
    user_id: int,
):
    task = await task_repository.get_task_by_id(
        db,
        task_id,
        user_id,
    )

    if task is None:
        raise TaskNotFoundException()

    return task


async def create_task(
    db: AsyncSession,
    task: TaskCreate,
    user_id: int,
):
    async with db.begin():
        new_task = await task_repository.create_task(
            db,
            task.title,
            task.completed,
            user_id,
        )

    await db.refresh(new_task)

    return new_task


async def update_task(
    db: AsyncSession,
    task_id: int,
    updated_task: TaskCreate,
    user_id: int,
):
    async with db.begin():
        task = await task_repository.get_task_by_id(
            db,
            task_id,
            user_id,
        )

        if task is None:
            raise TaskNotFoundException()

        task = await task_repository.update_task(
            db,
            task,
            updated_task.title,
            updated_task.completed,
        )

    await db.refresh(task)

    return task


async def patch_task(
    db: AsyncSession,
    task_id: int,
    updated_task: TaskUpdate,
    user_id: int,
):
    async with db.begin():
        task = await task_repository.get_task_by_id(
            db,
            task_id,
            user_id,
        )

        if task is None:
            raise TaskNotFoundException()

        changes = updated_task.model_dump(
            exclude_unset=True
        )

        task = await task_repository.patch_task(
            db,
            task,
            changes,
        )

    await db.refresh(task)

    return task


async def delete_task(
    db: AsyncSession,
    task_id: int,
    user_id: int,
):
    async with db.begin():
        task = await task_repository.get_task_by_id(
            db,
            task_id,
            user_id,
        )

        if task is None:
            raise TaskNotFoundException()

        await task_repository.delete_task(
            db,
            task,
        )