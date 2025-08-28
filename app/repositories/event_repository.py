from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models import AcademicEvent, Availability, Match, User, Club, Department, College


class EventRepository:
    def find_user_and_club(self, db: Session, user_id: str) -> Tuple[User, Club]:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            return None, None
        club = db.query(Club).filter(Club.club_id == user.club_id).first()
        return user, club

    def list_academic_events_by_college(self, db: Session, college_id: int) -> List[AcademicEvent]:
        return (
            db.query(AcademicEvent)
            .filter(AcademicEvent.college_id == college_id)
            .order_by(AcademicEvent.start_date.asc(), AcademicEvent.event_id.asc())
            .all()
        )

    def list_availability_by_club(self, db: Session, club_id: int) -> List[Availability]:
        return (
            db.query(Availability)
            .filter(Availability.club_id == club_id)
            .order_by(Availability.start_date.asc(), Availability.start_time.asc())
            .all()
        )

    def list_matches_by_club(self, db: Session, club_id: int) -> List[Match]:
        return (
            db.query(Match)
            .filter((Match.club_id == club_id) | (Match.club_id2 == club_id))
            .order_by(Match.date.asc(), Match.match_id.asc())
            .all()
        )


