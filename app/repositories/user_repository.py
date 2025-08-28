from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def exists_by_nickname(self, db: Session, nickname: str) -> bool:
        return (
            db.query(User.user_id)
            .filter(User.nickname == nickname)
            .limit(1)
            .first()
            is not None
        )

    def exists_by_user_id(self, db: Session, user_id: str) -> bool:
        return (
            db.query(User.user_id)
            .filter(User.user_id == user_id)
            .limit(1)
            .first()
            is not None
        )


