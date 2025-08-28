from sqlalchemy.orm import Session

from app.dto.api.response.nicknameCheckResponse import (
    NicknameCheckData,
    NicknameCheckResponse,
)
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def check_nickname(self, db: Session, nickname: str) -> NicknameCheckResponse:
        exists = self.repository.exists_by_nickname(db, nickname)
        is_valid = not exists
        return NicknameCheckResponse(
            status=200,
            message="중복 확인 성공",
            data=NicknameCheckData(isValid=is_valid),
        )

    def check_user_id(self, db: Session, user_id: str) -> "UserIdCheckResponse":
        from app.dto.api.response.userIdCheckResponse import (
            UserIdCheckData,
            UserIdCheckResponse,
        )

        exists = self.repository.exists_by_user_id(db, user_id)
        is_valid = not exists
        return UserIdCheckResponse(
            status=200,
            message="중복 확인 성공",
            data=UserIdCheckData(isValid=is_valid),
        )


