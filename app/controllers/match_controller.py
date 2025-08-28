from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.match.reqeust.matchAcceptRequest import MatchAcceptRequest
from app.dto.match.reqeust.matchCreateRequest import MatchCreateRequest
from app.dto.match.response.matchAcceptResponse import MatchAcceptResponse
from app.dto.match.response.matchRejectResponse import MatchRejectResponse
from app.repositories.match_repository import MatchRepository
from app.services.match_service import MatchService
from app.dto.match.response.matchListResponse import MatchListResponse
from app.dto.match.response.matchSuccessListResponse import MatchSuccessListResponse
from app.dto.match.response.matchRandomResponse import MatchRandomResponse
from app.dto.match.reqeust.matchRandomCreateRequest import MatchRandomCreateRequest
from app.dto.match.response.matchRandomCreateResponse import MatchRandomCreateResponse
from app.core.deps import get_current_user_id
from app.dto.match.response.matchCreateResponse import MatchCreateResponse


security = HTTPBearer(auto_error=True)
router = APIRouter(prefix="/match", tags=["match"], dependencies=[Depends(security)])


@router.post("/accept", response_model=MatchAcceptResponse)
def accept_match(
    body: MatchAcceptRequest, db: Session = Depends(get_db)
) -> MatchAcceptResponse:
    service = MatchService(MatchRepository())
    return service.accept_match(db, body)


@router.post("/reject", response_model=MatchRejectResponse)
def reject_match(
    body: MatchAcceptRequest, db: Session = Depends(get_db)
) -> MatchRejectResponse:
    service = MatchService(MatchRepository())
    return service.reject_match(db, body)


@router.get("/list", response_model=MatchListResponse)
def list_received_matches(
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)
) -> MatchListResponse:
    service = MatchService(MatchRepository())
    return service.list_received_requests(db, user_id)


@router.get("", response_model=MatchSuccessListResponse)
def list_success_matches(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)) -> MatchSuccessListResponse:
    service = MatchService(MatchRepository())
    return service.list_success_matches(db, user_id)


@router.post("/request", response_model=MatchCreateResponse)
def create_match_request(
    body: MatchCreateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> MatchCreateResponse:
    service = MatchService(MatchRepository())
    return service.create_friendly_request(db, user_id, body)


@router.post("/random", response_model=MatchRandomResponse)
def get_random_match(
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)
) -> MatchRandomResponse:
    service = MatchService(MatchRepository())
    return service.random_opponent(db, user_id)


@router.post("/random/request", response_model=MatchRandomCreateResponse)
def create_random_request(
    body: MatchRandomCreateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> MatchRandomCreateResponse:
    service = MatchService(MatchRepository())
    return service.random_request(db, user_id, body)
