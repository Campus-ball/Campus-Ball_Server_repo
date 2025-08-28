from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.availability.request.createAvailabilityRequest import (
    CreateAvailabilityRequest,
)
from app.dto.availability.response.createAvailabilityResponse import (
    CreateAvailabilityResponse,
)
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.user_repository import UserRepository
from app.core.deps import get_current_user_id
from app.services.availability_service import AvailabilityService


router = APIRouter(prefix="/availability", tags=["availability"]) 


@router.post("", response_model=CreateAvailabilityResponse)
def create_availability(
    req: CreateAvailabilityRequest = None,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> CreateAvailabilityResponse:
    service = AvailabilityService(AvailabilityRepository(), UserRepository())
    return service.create(db, user_id, req)
