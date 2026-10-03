from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task


async def get_tasks(
    db: AsyncSession,
    user_id: int,
    completed: bool | None = None,
    title: str | None = None,
):
    statement = select(Task).where(
        Task.user_id == user_id
    )

    if completed is not None:
        statement = statement.where(
            Task.completed == completed
        )

    if title is not None:
        statement = statement.where(
            Task.title.ilike(f"%{title}%")
        )

    result = await db.execute(statement)

    return result.scalars().all()


async def get_task_by_id(
    db: AsyncSession,
    task_id: int,
    user_id: int,
):
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,
    )

    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def create_task(
    db: AsyncSession,
    title: str,
    completed: bool,
    user_id: int,
):
    new_task = Task(
        title=title,
        completed=completed,
        user_id=user_id,
    )

    db.add(new_task)

    return new_task


async def update_task(
    db: AsyncSession,
    task: Task,
    title: str,
    completed: bool,
):
    task.title = title
    task.completed = completed

    return task


async def patch_task(
    db: AsyncSession,
    task: Task,
    changes: dict,
):
    for field, value in changes.items():
        setattr(task, field, value)

    return task


async def delete_task(
    db: AsyncSession,
    task: Task,
):
    await db.delete(task)