from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse
from app.services import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.register_user(
        db,
        user,
    )
    
@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.login_user(
        db,
        user,
    )