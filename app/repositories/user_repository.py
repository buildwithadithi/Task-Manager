from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def get_user_by_username(
    db: AsyncSession,
    username: str,
):
    statement = select(User).where(
        User.username == username
    )

    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    username: str,
    password_hash: str,
):
    new_user = User(
        username=username,
        password_hash=password_hash,
    )

    db.add(new_user)

    return new_user

async def get_user_by_id(
    db: AsyncSession,
    user_id: int,
):
    statement = select(User).where(
        User.id == user_id
    )

    result = await db.execute(statement)

    return result.scalar_one_or_none()