from typing import Optional, Tuple, List
from datetime import date, time

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Request, Club, Match, User, Department, Availability


class MatchRepository:
    def get_request_by_id(self, db: Session, request_id: int) -> Optional[Request]:
        return db.query(Request).filter(Request.request_id == request_id).first()

    def get_request_with_clubs(
        self, db: Session, request_id: int
    ) -> Tuple[Optional[Request], Optional[Club], Optional[Club]]:
        req = db.query(Request).filter(Request.request_id == request_id).first()
        if req is None:
            return None, None, None
        club1 = db.query(Club).filter(Club.club_id == req.club_id).first()
        club2 = db.query(Club).filter(Club.club_id == req.club_id2).first()
        return req, club1, club2

    def create_match_from_request(self, db: Session, req: Request) -> Match:
        match = Match(
            date=req.date,
            start_time=req.start_time,
            end_time=req.end_time,
            type=req.type,
            club_id=req.club_id,
            owner_id=req.owner_id,
            club_id2=req.club_id2,
            owner_id2=req.owner_id2,
        )
        db.add(match)
        db.flush()
        return match

    def delete_request(self, db: Session, req: Request) -> None:
        db.delete(req)

    def find_user_and_club(
        self, db: Session, user_id: str
    ) -> Tuple[Optional[User], Optional[Club]]:
        user = db.query(User).filter(User.user_id == user_id).first()
        club = (
            None
            if user is None
            else db.query(Club).filter(Club.club_id == user.club_id).first()
        )
        return user, club

    def list_received_requests(
        self, db: Session, club_id: int
    ) -> List[Tuple[Request, Club, Department]]:
        # Requests where this club is the receiver (club_id2)
        reqs = (
            db.query(Request, Club, Department)
            .join(Club, Club.club_id == Request.club_id)
            .join(Department, Department.department_id == Club.department_id)
            .filter(Request.club_id2 == club_id)
            .order_by(
                Request.date.asc(), Request.start_time.asc(), Request.request_id.asc()
            )
            .all()
        )
        return reqs

    def list_success_matches(
        self, db: Session, club_id: int
    ) -> List[Tuple[Match, Club, Department]]:
        rows = (
            db.query(Match, Club, Department)
            .join(Club, Club.club_id == Match.club_id)
            .join(Department, Department.department_id == Club.department_id)
            .filter((Match.club_id == club_id) | (Match.club_id2 == club_id))
            .order_by(Match.date.desc(), Match.start_time.desc(), Match.match_id.desc())
            .all()
        )
        return rows

    def create_friendly_request(
        self, db: Session, from_user_id: str, target_club_id: int
    ) -> None:
        user = db.query(User).filter(User.user_id == from_user_id).first()
        if user is None:
            raise ValueError("User not found")
        from_club = db.query(Club).filter(Club.club_id == user.club_id).first()
        to_club = db.query(Club).filter(Club.club_id == target_club_id).first()
        if from_club is None or to_club is None:
            raise ValueError("Club not found")
        req = Request(
            request_id=None,
            date=date.today(),
            start_time=time(17, 0),
            end_time=time(18, 0),
            type="친선 경기",
            club_id=from_club.club_id,
            owner_id=from_club.owner_id,
            club_id2=to_club.club_id,
            owner_id2=to_club.owner_id,
        )
        db.add(req)
        db.flush()
        return int(req.request_id)

    def create_random_request(
        self,
        db: Session,
        from_user_id: str,
        target_club_id: int,
        start_date: str,
        start_time: str,
        end_time: str,
    ) -> int:
        user = db.query(User).filter(User.user_id == from_user_id).first()
        if user is None:
            raise ValueError("User not found")
        from_club = db.query(Club).filter(Club.club_id == user.club_id).first()
        to_club = db.query(Club).filter(Club.club_id == target_club_id).first()
        if from_club is None or to_club is None:
            raise ValueError("Club not found")
        req = Request(
            request_id=None,
            date=start_date,
            start_time=start_time,
            end_time=end_time,
            type="랜덤 매칭 요청",
            club_id=from_club.club_id,
            owner_id=from_club.owner_id,
            club_id2=to_club.club_id,
            owner_id2=to_club.owner_id,
        )
        db.add(req)
        db.flush()
        return int(req.request_id)

    # Club + Match join: find clubs with fewer recent matches (example heuristic)
    def find_candidate_clubs_by_match(
        self, db: Session, exclude_club_id: int
    ) -> List[Tuple[Club, int]]:
        sub = (
            db.query(Match.club_id, func.count(Match.match_id).label("cnt"))
            .group_by(Match.club_id)
            .subquery()
        )
        rows = (
            db.query(Club, func.coalesce(sub.c.cnt, 0))
            .outerjoin(sub, sub.c.club_id == Club.club_id)
            .filter(Club.club_id != exclude_club_id)
            .order_by(sub.c.cnt.asc().nullsfirst(), Club.club_id.asc())
            .all()
        )
        return rows

    # Club + Availability join: find clubs that have any availability
    def find_candidate_slots_by_availability(
        self, db: Session, exclude_club_id: int
    ) -> List[Tuple[Club, Availability]]:
        rows = (
            db.query(Club, Availability)
            .join(Availability, Availability.club_id == Club.club_id)
            .filter(Club.club_id != exclude_club_id)
            .order_by(Availability.start_date.asc(), Availability.start_time.asc())
            .all()
        )
        return rows

    def find_my_availabilities(self, db: Session, club_id: int) -> List[Availability]:
        """현재 클럽의 가용시간 조회"""
        return (
            db.query(Availability)
            .filter(Availability.club_id == club_id)
            .order_by(Availability.start_date.asc(), Availability.start_time.asc())
            .all()
        )

    def find_clubs_with_matching_availability(
        self,
        db: Session,
        exclude_club_id: int,
        target_date: date,
        target_start_time: time,
        target_end_time: time,
    ) -> List[Tuple[Club, Availability, int]]:
        """같은 날짜에 가용시간이 있는 다른 클럽들 찾기 (경기 수 포함)"""
        # 경기 수 서브쿼리
        match_sub = (
            db.query(Match.club_id, func.count(Match.match_id).label("cnt"))
            .group_by(Match.club_id)
            .subquery()
        )

        rows = (
            db.query(Club, Availability, func.coalesce(match_sub.c.cnt, 0))
            .join(Availability, Availability.club_id == Club.club_id)
            .outerjoin(match_sub, match_sub.c.club_id == Club.club_id)
            .filter(
                Club.club_id != exclude_club_id, Availability.start_date == target_date
            )
            .order_by(match_sub.c.cnt.asc().nullsfirst(), Club.club_id.asc())
            .all()
        )
        return rows
