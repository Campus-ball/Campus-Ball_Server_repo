from functools import lru_cache
from typing import List, Optional
import json

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

    # CORS (avoid List[str] field binding directly from env to prevent JSON decode issues)
    cors_origins_env: Optional[str] = Field(default=None, alias="CORS_ORIGINS")

    # Locale
    timezone: str = Field(default="Asia/Seoul", alias="TZ")

    # File uploads
    files_dir: str = Field(default="/data/files", alias="FILES_DIR")
    files_base_url: str = Field(
        default="http://campus-ball-server.kro.kr:30080/files", alias="FILES_BASE_URL"
    )

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

    def parse_cors_origins(self) -> List[str]:
        raw = self.cors_origins_env
        if raw is None:
            return []
        s = raw.strip()
        if s == "" or s == "[]":
            return []
        if s == "*":
            return ["*"]
        if s.startswith("["):
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return [str(x) for x in parsed]
            except Exception:
                return []
        return [item.strip() for item in s.split(",") if item.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
