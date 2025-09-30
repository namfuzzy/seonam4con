from functools import lru_cache
from typing import List

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    app_name: str = "SEO nội bộ"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    algorithm: str = "HS256"

    app_secret: str = "dev-app-secret-change"

    backend_cors_origins: List[str] | str = []

    database_url: str = "sqlite+aiosqlite:///./app.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i]
        if isinstance(v, list):
            return v
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()
