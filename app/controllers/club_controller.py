from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user_id
from app.dto.club.request.clubInfoResponse import ClubInfoResponse
from app.repositories.club_repository import ClubRepository
from app.services.club_service import ClubService


router = APIRouter(prefix="/club", tags=["club"])


@router.get("/{club_id}", response_model=ClubInfoResponse)
def get_club_info(club_id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)) -> ClubInfoResponse:
    service = ClubService(ClubRepository())
    return service.get_club_info(db, my_user_id=user_id, opponent_club_id=club_id)
