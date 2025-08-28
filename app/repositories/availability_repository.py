from sqlalchemy.orm import Session

from app.models import Availability


class AvailabilityRepository:
    def create(
        self,
        db: Session,
        *,
        club_id: int,
        owner_id: str,
        start_date: str,
        start_time: str,
        end_time: str,
    ) -> int:
        entity = Availability(
            club_id=club_id,
            owner_id=owner_id,
            start_date=start_date,
            start_time=start_time,
            end_time=end_time,
        )
        db.add(entity)
        db.flush()
        return int(entity.availability_id)
