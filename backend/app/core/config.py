from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    app_name: str = "SEO Nội Bộ"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(..., env="APP_SECRET")
    jwt_secret_key: str = Field(..., env="JWT_SECRET")
    jwt_refresh_secret_key: str = Field(..., env="JWT_REFRESH_SECRET")
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 7
    backend_cors_origins: List[str] = Field(default_factory=list)
    database_url: PostgresDsn = Field(..., env="DATABASE_URL")
    environment: str = Field("development", env="ENVIRONMENT")

    class Config:
        case_sensitive = True
        env_file = None

    @validator("backend_cors_origins", pre=True)
    def assemble_cors(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache()
def get_settings() -> Settings:
    return Settings()
