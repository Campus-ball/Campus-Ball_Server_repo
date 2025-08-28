from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.dto.user.response.userMeResponse import UserMeResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


security = HTTPBearer(auto_error=True)
router = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(security)])


@router.get("/me", response_model=UserMeResponse)
def get_me(
    db: Session = Depends(get_db), authorization: str = Depends(lambda: ""),
) -> UserMeResponse:
    from app.core.settings import get_settings
    from jose import jwt

    settings = get_settings()
    if not authorization or not authorization.lower().startswith("bearer "):
        return UserMeResponse(
            status=401,
            message="인증 실패",
            data=None,
        )
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_alg])
        user_id = payload.get("sub", "")
    except Exception:
        return UserMeResponse(
            status=401,
            message="인증 실패",
            data=None,
        )
    service = UserService(UserRepository())
    return service.get_me(db, user_id)
