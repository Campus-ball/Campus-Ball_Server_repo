from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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
from app.services.availability_service import AvailabilityService


router = APIRouter(prefix="/availability", tags=["availability"])
security = HTTPBearer(auto_error=True)


@router.post("/", response_model=CreateAvailabilityResponse)
def create_availability(
    cred: HTTPAuthorizationCredentials = Depends(security),
    req: CreateAvailabilityRequest = None,
    db: Session = Depends(get_db),
) -> CreateAvailabilityResponse:
    service = AvailabilityService(AvailabilityRepository(), UserRepository())
    return service.create(db, cred.credentials, req)
