from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models import Club, Department, AcademicEvent, Availability, Match, User


class ClubRepository:
    def find_user_and_club(self, db: Session, user_id: str) -> Tuple[Optional[User], Optional[Club]]:
        user = db.query(User).filter(User.user_id == user_id).first()
        club = None if user is None else db.query(Club).filter(Club.club_id == user.club_id).first()
        return user, club

    def get_opponent_with_department(self, db: Session, club_id: int) -> Tuple[Optional[Club], Optional[Department]]:
        club = db.query(Club).filter(Club.club_id == club_id).first()
        dept = None
        if club:
            dept = db.query(Department).filter(Department.department_id == club.department_id).first()
        return club, dept

    def list_academic_events_by_club(self, db: Session, club: Club) -> List[AcademicEvent]:
        dept = db.query(Department).filter(Department.department_id == club.department_id).first()
        if not dept:
            return []
        return (
            db.query(AcademicEvent)
            .filter(AcademicEvent.college_id == dept.college_id)
            .order_by(AcademicEvent.start_date.asc(), AcademicEvent.event_id.asc())
            .all()
        )

    def list_availability_by_club(self, db: Session, club_id: int) -> List[Availability]:
        return (
            db.query(Availability)
            .filter(Availability.club_id == club_id)
            .order_by(Availability.start_date.asc(), Availability.availability_id.asc())
            .all()
        )

    def list_matches_by_club(self, db: Session, club_id: int) -> List[Match]:
        return (
            db.query(Match)
            .filter((Match.club_id == club_id) | (Match.club_id2 == club_id))
            .order_by(Match.date.asc(), Match.match_id.asc())
            .all()
        )

    def list_all(self, db: Session) -> List[Club]:
        return db.query(Club).order_by(Club.club_id.asc()).all()

