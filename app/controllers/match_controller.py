from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.match.reqeust.matchAcceptRequest import MatchAcceptRequest
from app.dto.match.response.matchAcceptResponse import MatchAcceptResponse
from app.dto.match.response.matchRejectResponse import MatchRejectResponse
from app.repositories.match_repository import MatchRepository
from app.services.match_service import MatchService
from app.dto.match.response.matchListResponse import MatchListResponse
from app.core.settings import get_settings
from jose import jwt


router = APIRouter(prefix="/api", tags=["match"])


@router.post("/match/accept", response_model=MatchAcceptResponse)
def accept_match(body: MatchAcceptRequest, db: Session = Depends(get_db)) -> MatchAcceptResponse:
    service = MatchService(MatchRepository())
    return service.accept_match(db, body)


@router.post("/match/reject", response_model=MatchRejectResponse)
def reject_match(body: MatchAcceptRequest, db: Session = Depends(get_db)) -> MatchRejectResponse:
    service = MatchService(MatchRepository())
    return service.reject_match(db, body)


@router.get("/match/list", response_model=MatchListResponse)
def list_received_matches(db: Session = Depends(get_db), authorization: str = Header(default="")) -> MatchListResponse:
    settings = get_settings()
    if not authorization or not authorization.lower().startswith("bearer "):
        return MatchListResponse(status=500, message="받은 신청 목록을 가져오는데 실패했습니다.", data={"items": []})
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_alg])
        user_id = payload.get("sub", "")
    except Exception:
        user_id = ""
    service = MatchService(MatchRepository())
    return service.list_received_requests(db, user_id)


