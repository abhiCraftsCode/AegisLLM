from fastapi import HTTPException,status
from sqlalchemy import or_,select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import RegisterSchema,AuthResponse,LoginSchema,TokenSchema,ProfileSchema
from app.models import User
from app.core.security import hash_password,create_jwt_token,verify_password

class AuthService:
  """provides all services related to authentication"""

  @staticmethod
  async def register_user(data:RegisterSchema,db:AsyncSession)->AuthResponse:
    """register a new user."""
    
    #check if credentials are available
    if data.email is None and data.phone is None:
      raise HTTPException(detail="Missing credentials. Enter either email or phone.",
                          status_code=status.HTTP_400_BAD_REQUEST)

    # check if user already exist with those credentials
    condition=[]
    if data.email:
      condition.append(User.email==data.email)
    if data.phone:
      condition.append(User.phone==data.phone)
    stmt=select(User).where(or_(*condition))
    existing_user=(await db.execute(stmt)).scalar_one_or_none()
    if existing_user is not None:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Another User already exists.")

    # creating new user
    new_user=User(
      name=data.name,
      email=data.email,
      phone=data.phone,
      hash_password=hash_password(data.password)
    )
    # inserting and commiting to database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)#new user data here

    # issue tokens for session management
    access_token=create_jwt_token(id=new_user.id,token_type="access")
    refresh_token=create_jwt_token(id=new_user.id,token_type="refresh")

    return AuthResponse(
      user=ProfileSchema.model_validate(new_user),
      tokens=TokenSchema(access_token=access_token,refresh_token=refresh_token)
    )

  @staticmethod
  async def login_user(data:LoginSchema,db:AsyncSession)->AuthResponse:
    """login a existing user."""

    #check for user availability
    identifier=data.identifier.strip()
    stmt=select(User).where(or_(User.email==identifier,User.phone==identifier))
    user=(await db.execute(stmt)).scalar_one_or_none()
    # invalid identifier / oauth user but trying login by password / invalid password
    if user is None or user.hash_password is None or not verify_password(data.password,user.hash_password):
      raise HTTPException(detail="Invalid credentials.",status_code=status.HTTP_401_UNAUTHORIZED)

    # issue tokens for session management
    access_token=create_jwt_token(id=user.id,token_type="access")
    refresh_token=create_jwt_token(id=user.id,token_type="refresh")

    return AuthResponse(
      user=ProfileSchema.model_validate(user),
      tokens=TokenSchema(access_token=access_token,refresh_token=refresh_token)
    )