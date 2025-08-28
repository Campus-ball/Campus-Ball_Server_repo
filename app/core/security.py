from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Dict

from passlib.context import CryptContext
from jose import jwt

from app.core.settings import get_settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)


def verify_password(pw: str, hashed: str) -> bool:
    return pwd_ctx.verify(pw, hashed)


def create_access_token(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": sub, "exp": exp}
    if settings.jwt_alg == "HS256":
        return jwt.encode(payload, settings.secret_key, algorithm="HS256")
    # RS256인 경우 키 로딩 생략
    raise NotImplementedError("RS256 키 로딩 구현 필요")


def create_refresh_token(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=settings.refresh_token_expire_minutes
    )
    payload = {"sub": sub, "exp": exp, "type": "refresh"}
    if settings.jwt_alg == "HS256":
        return jwt.encode(payload, settings.secret_key, algorithm="HS256")
    raise NotImplementedError("RS256 키 로딩 구현 필요")


def generate_secret_key(num_bytes: int = 32) -> str:
    return token_urlsafe(num_bytes)


def create_token_pair(sub: str) -> Dict[str, str]:
    return {
        "access_token": create_access_token(sub),
        "refresh_token": create_refresh_token(sub),
        "token_type": "bearer",
    }
