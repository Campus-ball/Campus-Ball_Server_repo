from typing import List

from sqlalchemy.orm import Session

from app.models import College


class CollageRepository:
    def list_all(self, db: Session) -> List[College]:
        return db.query(College).order_by(College.college_id.asc()).all()


