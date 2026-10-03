from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserLogin, TokenResponse
from app.repositories import user_repository
from app.security import hash_password, verify_password, create_access_token
from app.exception_handler import UserAlreadyExistsException, InvalidCredentialsException


async def register_user(
    db: AsyncSession,
    user: UserCreate,
):
    password_hash = hash_password(user.password)

    async with db.begin():

        existing_user = await user_repository.get_user_by_username(
            db,
            user.username,
        )

        if existing_user is not None:
            raise UserAlreadyExistsException()

        new_user = await user_repository.create_user(
            db,
            user.username,
            password_hash,
        )

    await db.refresh(new_user)

    return new_user

async def login_user(
    db: AsyncSession,
    user: UserLogin,
):
    existing_user = await user_repository.get_user_by_username(
        db,
        user.username,
    )

    if existing_user is None:
        raise InvalidCredentialsException()

    if not verify_password(
        user.password,
        existing_user.password_hash,
    ):
        raise InvalidCredentialsException()

    token = create_access_token(existing_user.id)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )