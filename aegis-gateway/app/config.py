import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aegis Security Gateway"
    VERSION: str = "1.0.0"
    
    # Database Settings (Defaults to local SQLite for fast dev testing)
    DATABASE_URL: str = "sqlite+aiosqlite:///./aegis.db"
    
    # Model Configuration
    MODEL_PATH: str = os.path.join("models", "aegis_model.onnx")
    THREAT_BLOCK_THRESHOLD: float = 0.50
    
    # Default Rate Limit
    DEFAULT_RATE_LIMIT_RPM: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()