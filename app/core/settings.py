from functools import lru_cache
from typing import List, Optional

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # App
    app_name: str = Field(default="campusball", alias="APP_NAME")
    env: str = Field(default="development", alias="ENV")
    debug: bool = Field(default=True, alias="DEBUG")

    # Database (primary SQL DB)
    database_url: Optional[AnyUrl] = Field(default=None, alias="DATABASE_URL")
    sqlalchemy_database_url: Optional[AnyUrl] = Field(
        default=None, alias="SQLALCHEMY_DATABASE_URL"
    )
    sqlalchemy_echo: bool = Field(default=False, alias="SQLALCHEMY_ECHO")

    # Security / Auth
    secret_key: str = Field(alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(
        default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    jwt_alg: str = Field(default="HS256", alias="JWT_ALG")
    refresh_token_expire_minutes: int = Field(
        default=60 * 24 * 14, alias="REFRESH_TOKEN_EXPIRE_MINUTES"
    )

    # CORS
    cors_origins: List[str] = Field(default_factory=list, alias="CORS_ORIGINS")

    # Locale
    timezone: str = Field(default="Asia/Seoul", alias="TZ")

    # Optional MongoDB
    mongo_database_url: Optional[str] = Field(default=None, alias="MONGO_DATABASE_URL")
    mongo_db_name: Optional[str] = Field(default=None, alias="MONGO_DB_NAME")

    # Compatibility accessor
    @property
    def resolved_database_url(self) -> str:
        if self.database_url is not None:
            return str(self.database_url)
        if self.sqlalchemy_database_url is not None:
            return str(self.sqlalchemy_database_url)
        raise ValueError(
            "DATABASE_URL or SQLALCHEMY_DATABASE_URL must be set in environment"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
