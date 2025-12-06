from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ENV: str = "development"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Postgres
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "appdb"
    DATABASE_USER: str = "app"
    DATABASE_PASSWORD: str = "password"
    DATABASE_URL: Optional[str] = None

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_url(cls, v, info):
        if v is not None:
            return str(v)
        data = info.data
        return f"postgresql://{data.get('DATABASE_USER')}:{data.get('DATABASE_PASSWORD')}@" \
               f"{data.get('DATABASE_HOST')}:{data.get('DATABASE_PORT')}/{data.get('DATABASE_NAME')}"

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
