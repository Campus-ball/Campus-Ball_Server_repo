from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.event.response.eventListResponse import EventListResponse
from app.repositories.event_repository import EventRepository
from app.services.event_service import EventService
from app.core.deps import get_current_user_id


router = APIRouter(prefix="/event", tags=["event"])


@router.get("/list", response_model=EventListResponse)
def list_events(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)) -> EventListResponse:
    service = EventService(EventRepository())
    return service.list_events_for_user(db, user_id)
