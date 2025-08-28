from sqlalchemy.orm import Session
from app.dto.api.response.nicknameCheckResponse import (
    NicknameCheckData,
    NicknameCheckResponse,
)
from app.dto.user.response.userMeResponse import UserMeData, UserMeResponse
from app.repositories.user_repository import UserRepository
from app.dto.api.response.userIdCheckResponse import (
    UserIdCheckData,
    UserIdCheckResponse,
)


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
            UserIdCheckResponse,
        )

        exists = self.repository.exists_by_user_id(db, user_id)
        is_valid = not exists
        return UserIdCheckResponse(
            status=200,
            message="중복 확인 성공",
            data=UserIdCheckData(isValid=is_valid),
        )

    def get_me(self, db: Session, user_id: str) -> UserMeResponse:
        user, club = self.repository.get_user_with_club(db, user_id)
        if user is None:
            raise ValueError("User not found")
        return UserMeResponse(
            status=200,
            message="나의 정보를 불러왔습니다.",
            data=UserMeData(
                name=user.name,
                nickname=user.nickname,
                gender=user.gender,
                clubName=club.name if club else None,
                phoneNumber=user.phone_number,
                chatUrl=club.chat_url if club else None,
            ),
        )
