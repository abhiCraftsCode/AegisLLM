from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.token.service import TokenService
from app.modules.auth.repository import UserRepository
from app.models import User
from app.db.session import get_db


bearer_scheme = HTTPBearer()


#dependency helper function to implement isAuth
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """dependency for is_auth, fetches the logged in user."""
    token = credentials.credentials

    payload = TokenService.decode_token(token)

    # chechk if token decoded successfully
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    # check if token is access token
    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )

    user_id = payload.id
    repository = UserRepository(db)

    user = await repository.get_by_id(user_id)

    #check if user of that id found
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user