from typing import List

from sqlalchemy.orm import Session

from app.models import Club


class ClubRepository:
    def list_all(self, db: Session) -> List[Club]:
        return db.query(Club).order_by(Club.club_id.asc()).all()


