from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.event.response.eventListResponse import EventListResponse
from app.repositories.event_repository import EventRepository
from app.services.event_service import EventService
from app.core.settings import get_settings
from jose import jwt


router = APIRouter(prefix="/event", tags=["event"])


@router.get("/list", response_model=EventListResponse)
def list_events(
    db: Session = Depends(get_db), authorization: str = Header(default="")
) -> EventListResponse:
    settings = get_settings()
    if not authorization or not authorization.lower().startswith("bearer "):
        return EventListResponse(
            status=200,
            message="캘린더 이벤트를 성공적으로 가져왔습니다.",
            data={"items": []},
        )
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_alg])
        user_id = payload.get("sub", "")
    except Exception:
        user_id = ""
    service = EventService(EventRepository())
    return service.list_events_for_user(db, user_id)
