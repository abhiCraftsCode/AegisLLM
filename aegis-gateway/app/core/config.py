from typing import List,ClassVar,Optional
from pydantic import Field,SecretStr
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
  """class to configure the app settings from env file."""

  # App Metadata (Hardcoded constants)
  PROJECT_NAME: str = "Aegis-gateway"
  PROJECT_VERSION: str = "1.0.0"
  ALGORITHM: str = "HS256"

  # Gateway & Security Policy (Tuneable via .env, with safe defaults)
  THREAT_BLOCK_THRESHOLD: float = 0.80
  DEFAULT_RATE_LIMIT_RPM: int = 60
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 360
  REFRESH_TOKEN_EXPIRE_DAYS: int = 2
  RESET_TOKEN_EXPIRE_MINUTES: int = 15
  LOCAL_MODEL_PATH:Optional[str] = None

  # Mandatory Application Secrets & Endpoints (Must be in .env)
  DATABASE_URL: str = Field(...)
  SECRET_KEY: str = Field(...)
  ENCRYPTION_KEY: str = Field(...)
  FRONTEND_URL: str = Field(...)
  ALLOWED_ORIGINS: List[str] = Field(...)

  # Hugging Face Model Loader
  HF_REPO_ID: str = Field(...)
  HF_MODEL_NAME: str = Field(...)

  # OAuth Credentials
  GOOGLE_CLIENT_ID: str = Field(...)
  GOOGLE_CLIENT_SECRET: SecretStr = Field(...)
  GOOGLE_REDIRECT_URI: str = Field(...)
  GITHUB_CLIENT_ID: str = Field(...)
  GITHUB_CLIENT_SECRET: SecretStr = Field(...)
  GITHUB_REDIRECT_URI: str = Field(...)

  # OAuth Fixed Provider Endpoints (ClassVar - never read from .env)
  GOOGLE_TOKEN_URL: ClassVar[str] = "https://oauth2.googleapis.com/token"
  GOOGLE_USERINFO_URL: ClassVar[str] = "https://www.googleapis.com/oauth2/v3/userinfo"
  GITHUB_TOKEN_URL: ClassVar[str] = "https://github.com/login/oauth/access_token"
  GITHUB_USERINFO_URL: ClassVar[str] = "https://api.github.com/user"
  GITHUB_EMAILS_URL: ClassVar[str] = "https://api.github.com/user/emails"

  # Mail Server Configuration
  MAIL_USERNAME: str = "AegisLLM"
  MAIL_FROM_NAME: str = "AegisLLM"
  MAIL_SERVER: str = "smtp.gmail.com"
  MAIL_STARTTLS: bool = True
  MAIL_SSL_TLS: bool = False
  USE_CREDENTIALS: bool = True
  VALIDATE_CERTS: bool = True
  MAIL_PORT: int = 587
  MAIL_FROM: str = Field(...)
  MAIL_PASSWORD: SecretStr = Field(...)

  #env configuration can be done in 2 ways
  #v2 pydantic
  model_config=SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    env_file_encoding='utf-8'
    )
  #v1 pydantic
  # class Config:
  #   env_file=".env"
  #   extra="ignore"


settings=Settings() #type:ignore //requiring fields not available error bcz of editor type checks