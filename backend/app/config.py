import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ROI Calculator & Financial Engine"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./roi_calculator.db")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "chave_secreta_desenvolvimento_123456789")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    CORS_ORIGINS: list = ["*"]

    class Config:
        case_sensitive = True

settings = Settings()
