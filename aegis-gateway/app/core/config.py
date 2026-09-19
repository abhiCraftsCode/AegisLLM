from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  """class to configure the app settings from env file."""

  PROJECT_NAME:str="Aegis-gateway"
  PROJECT_VERSION:str="1.0.0"
  THREAT_BLOCK_THRESHOLD:float=0.80
  DEFAULT_RATE_LIMIT_RPM:int=60
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 360
  REFRESH_TOKEN_EXPIRE_DAYS: int = 2
  RESET_TOKEN_EXPIRE_MINUTES:int = 15

  # mandatories
  DATABASE_URL:str=Field(...)
  MODEL_PATH:str=Field(...)
  SECRET_KEY:str=Field(...)
  GATEWAY_KEY:str=Field(...)
  ALLOWED_ORIGINS: List[str] = Field(...)

  #env configuration can be done in 2 ways
  #config=SettingsConfigDict(env_file=".env",extra="ignore")
  class Config:
    env_file=".env"
    extra="ignore"


settings=Settings() #type:ignore //requiring fields not available error bcz of editor type checks