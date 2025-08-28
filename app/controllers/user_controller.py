from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.dto.user.response.userMeResponse import UserMeResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


router = APIRouter(prefix="/user", tags=["user"])
security = HTTPBearer(auto_error=True)


@router.get("/me", response_model=UserMeResponse)
def get_me(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserMeResponse:
    token = cred.credentials
    payload = decode_token(token)
    user_id = payload.get("sub")
    service = UserService(UserRepository())
    return service.get_me(db, user_id)
