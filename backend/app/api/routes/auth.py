from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginRequest, Token
from app.services.auth import authenticate_user, login_for_tokens
from app.db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)) -> Token:
    user = await authenticate_user(session, data.email, data.password)
    tokens = await login_for_tokens(user)
    return Token(**tokens)
