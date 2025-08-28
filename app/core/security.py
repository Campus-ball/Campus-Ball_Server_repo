from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Dict
from uuid import uuid4

from passlib.context import CryptContext
from jose import jwt, JWTError

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
    payload = {"sub": sub, "exp": exp, "jti": str(uuid4()), "type": "access"}
    if settings.jwt_alg == "HS256":
        return jwt.encode(payload, settings.secret_key, algorithm="HS256")
    # RS256인 경우 키 로딩 생략
    raise NotImplementedError("RS256 키 로딩 구현 필요")


def create_refresh_token(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=settings.refresh_token_expire_minutes
    )
    payload = {"sub": sub, "exp": exp, "type": "refresh", "jti": str(uuid4())}
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


def decode_token(token: str) -> Dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_alg])
    except JWTError as e:
        raise ValueError("Invalid token") from e
