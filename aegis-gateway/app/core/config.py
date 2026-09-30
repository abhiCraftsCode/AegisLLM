from typing import List,ClassVar
from pydantic import Field,SecretStr
from pydantic_settings import BaseSettings,SettingsConfigDict

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

  # OAuth fields  
<<<<<<< HEAD
  GOOGLE_TOKEN_URL:ClassVar[str] = "https://oauth2.googleapis.com/token"
  GOOGLE_USERINFO_URL:ClassVar[str] = "https://www.googleapis.com/oauth2/v3/userinfo"
  GOOGLE_CLIENT_ID: str = Field(...)
  GOOGLE_CLIENT_SECRET: SecretStr = Field(...)#if error do .getsecret() 
  GOOGLE_REDIRECT_URI: str = Field(...)

  GITHUB_TOKEN_URL:ClassVar[str] = "https://github.com/login/oauth/access_token"
  GITHUB_USERINFO_URL:ClassVar[str] = "https://api.github.com/user"
  GITHUB_EMAILS_URL:str = "https://api.github.com/user/emails"
  GITHUB_CLIENT_ID: str = Field(...)
  GITHUB_CLIENT_SECRET: SecretStr = Field(...) #if error do .getsecret() 
  GITHUB_REDIRECT_URI: str = Field(...)
=======
  GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
  GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
  GOOGLE_CLIENT_ID: str = Field(...)
  GOOGLE_CLIENT_SECRET: SecretStr = Field(...)
  GOOGLE_REDIRECT_URI: str = "http://localhost:5173/auth/callback/google"

  GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
  GITHUB_USER_URL = "https://api.github.com/user"
  GITHUB_EMAILS_URL = "https://api.github.com/user/emails"
  GITHUB_CLIENT_ID: str = Field(...)
  GITHUB_CLIENT_SECRET: SecretStr = Field(...)
  GITHUB_REDIRECT_URI: str = "http://localhost:5173/auth/callback/github"
>>>>>>> 17d9fee965e0c36de9e1f1f3c0e0f3435298c0a1

  #mail service #mandatory
  MAIL_USERNAME:str = "AegisLLM"
  # vimp i have to revoke and get new app password for mail old compromised
  MAIL_PASSWORD:SecretStr= Field(...) #always use app password not original password
  MAIL_FROM:str = Field(...)
  MAIL_PORT:int = 587
  MAIL_SERVER:str = Field(...)
  MAIL_FROM_NAME:str="AegisLLM"
  MAIL_STARTTLS:bool = True
  MAIL_SSL_TLS:bool = False
  USE_CREDENTIALS:bool = True
  VALIDATE_CERTS:bool = True

  # mandatories
  DATABASE_URL:str=Field(...)
  MODEL_PATH:str=Field(...)
  SECRET_KEY:str=Field(...)
  ENCRYPTION_KEY:str=Field(...)
  GATEWAY_KEY:str=Field(...)
  ALLOWED_ORIGINS: List[str] = Field(...)
  FRONTEND_URL:str=Field(...)

  #env configuration can be done in 2 ways
  #v2 pydantic
  model_config=SettingsConfigDict(env_file=".env",extra="ignore")
  #v1 pydantic
  # class Config:
  #   env_file=".env"
  #   extra="ignore"


settings=Settings() #type:ignore //requiring fields not available error bcz of editor type checks