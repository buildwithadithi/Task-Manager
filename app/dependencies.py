from fastapi import Depends
from app.database import AsyncSessionLocal
from app.models import User
from app.repositories import user_repository
from fastapi.security import HTTPAuthorizationCredentials
from app.security import (
    bearer_scheme,
    decode_access_token,
)
from app.exceptions import InvalidCredentialsException

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:

    token = credentials.credentials

    payload = decode_access_token(token)

    user_id = int(payload["sub"])

    async with AsyncSessionLocal() as db:
        user = await user_repository.get_user_by_id(
            db,
            user_id,
        )

        if user is None:
            raise InvalidCredentialsException()

        return user