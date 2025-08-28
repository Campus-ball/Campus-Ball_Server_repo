from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user_id
from app.dto.user.response.userMeResponse import UserMeResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


router = APIRouter(prefix="/user", tags=["user"]) 


@router.get("/me", response_model=UserMeResponse)
def get_me(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)) -> UserMeResponse:
    service = UserService(UserRepository())
    return service.get_me(db, user_id)
