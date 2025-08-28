from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.dto.availability.request.createAvailabilityRequest import (
    CreateAvailabilityRequest,
)
from app.dto.availability.response.createAvailabilityResponse import (
    CreateAvailabilityData,
    CreateAvailabilityResponse,
)
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.user_repository import UserRepository


class AvailabilityService:
    def __init__(
        self, availability_repo: AvailabilityRepository, user_repo: UserRepository
    ):
        self.availability_repo = availability_repo
        self.user_repo = user_repo

    def create(
        self, db: Session, token: str, req: CreateAvailabilityRequest
    ) -> CreateAvailabilityResponse:
        payload = decode_token(token)
        user_id = payload.get("sub")
        user, _ = self.user_repo.get_user_with_club(db, user_id)
        if user is None:
            raise ValueError("User not found")
        # weekly recurring handling (default 8 weeks)
        first_id: int | None = None
        if req.isRecurring:
            base_date = datetime.strptime(req.startDate, "%Y-%m-%d").date()
            for week in range(8):
                d = (base_date + timedelta(days=7 * week)).isoformat()
                new_id = self.availability_repo.create(
                    db,
                    club_id=user.club_id,
                    owner_id=user.user_id,
                    start_date=d,
                    start_time=req.startTime,
                    end_time=req.endTime,
                )
                if first_id is None:
                    first_id = new_id
        else:
            first_id = self.availability_repo.create(
                db,
                club_id=user.club_id,
                owner_id=user.user_id,
                start_date=req.startDate,
                start_time=req.startTime,
                end_time=req.endTime,
            )
        return CreateAvailabilityResponse(
            status=200,
            message="경기 가용 시간이 성공적으로 등록되었습니다.",
            data=CreateAvailabilityData(
                availabilityId=int(first_id) if first_id is not None else 0
            ),
        )
