from sqlalchemy.orm import Session

from app.models import Club, Department, User


class AuthRepository:
    def find_user_by_id(self, db: Session, user_id: str) -> User | None:
        return db.get(User, user_id)

    def create_user_and_club(
        self,
        db: Session,
        *,
        user_id: str,
        password_hash: str,
        name: str,
        nickname: str,
        phone_number: str,
        gender: str,
        college_id: int,
        department_id: int,
        club_name: str,
        club_description: str,
        club_logo_url: str | None,
        chat_url: str | None,
    ) -> None:
        # 부서 유효성 체크 (존재 확인). 필요 시 college_id 활용한 추가 검증 확장 가능
        department = db.get(Department, department_id)
        if department is None:
            raise ValueError("Invalid departmentId")

        user = User(
            user_id=user_id,
            password_hash=password_hash,
            name=name,
            nickname=nickname,
            phone_number=phone_number,
            gender=gender,
            role="OWNER",
            club_id=0,  # 임시, 클럽 생성 후 업데이트
        )
        db.add(user)
        db.flush()

        club = Club(
            club_id=None,  # Auto-increment 가정; DB 측에서 할당된다면 None
            owner_id=user_id,
            name=club_name,
            description=club_description,
            logo_img_url=club_logo_url,
            chat_url=chat_url,
            department_id=department_id,
        )
        db.add(club)
        db.flush()

        # 생성된 club_id를 사용자에 반영
        user.club_id = club.club_id

        db.commit()
