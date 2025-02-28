from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from typing import List
import os


load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    DEBUG: bool = False
    CORS_ORIGINS: List = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
    ]
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()