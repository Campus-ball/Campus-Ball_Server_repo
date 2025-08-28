from typing import Optional, Tuple, List

from sqlalchemy.orm import Session

from app.models import Request, Club, Match, User, Department


class MatchRepository:
    def get_request_by_id(self, db: Session, request_id: int) -> Optional[Request]:
        return db.query(Request).filter(Request.request_id == request_id).first()
    def get_request_with_clubs(self, db: Session, request_id: int) -> Tuple[Optional[Request], Optional[Club], Optional[Club]]:
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

    def find_user_and_club(self, db: Session, user_id: str) -> Tuple[Optional[User], Optional[Club]]:
        user = db.query(User).filter(User.user_id == user_id).first()
        club = None if user is None else db.query(Club).filter(Club.club_id == user.club_id).first()
        return user, club

    def list_received_requests(self, db: Session, club_id: int) -> List[Tuple[Request, Club, Department]]:
        # Requests where this club is the receiver (club_id2)
        reqs = (
            db.query(Request, Club, Department)
            .join(Club, Club.club_id == Request.club_id)
            .join(Department, Department.department_id == Club.department_id)
            .filter(Request.club_id2 == club_id)
            .order_by(Request.date.asc(), Request.start_time.asc(), Request.request_id.asc())
            .all()
        )
        return reqs


