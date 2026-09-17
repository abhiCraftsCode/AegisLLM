from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.token.service import TokenService
from app.modules.user.service import UserService
from app.modules.user.schemas import ProfileSchema
from app.db.session import get_db
from app.core.exceptions import MissingTokenError,AccessTokenError

bearer_scheme = HTTPBearer()

#dependency helper function to implement isAuth
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> ProfileSchema:
    """dependency for is_auth, fetches the profile of logged in user."""

    token = credentials.credentials

    # chechk if token decodesuccessfully
    if token is None or len(token)==0:
        raise MissingTokenError()

    payload = TokenService.decode_token(token)

    # check if token is access token
    if payload.type != "access":
        raise AccessTokenError()

    user_id = payload.id
    user = await UserService.get_profile(user_id,db)

    return user