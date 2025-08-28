from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.settings import get_settings
from app.dto.club.request.clubInfoResponse import ClubInfoResponse
from app.repositories.club_repository import ClubRepository
from app.services.club_service import ClubService
from jose import jwt


router = APIRouter(prefix="/api", tags=["club"])


@router.get("/club/{club_id}", response_model=ClubInfoResponse)
def get_club_info(club_id: int, db: Session = Depends(get_db), authorization: str = Header(default="")) -> ClubInfoResponse:
    settings = get_settings()
    user_id = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_alg])
            user_id = payload.get("sub", "")
        except Exception:
            user_id = ""
    service = ClubService(ClubRepository())
    return service.get_club_info(db, my_user_id=user_id, opponent_club_id=club_id)


