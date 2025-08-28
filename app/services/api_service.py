from sqlalchemy.orm import Session
from fastapi import UploadFile
import os
import uuid

from app.dto.api.response.collageListResponse import CollegeListResponse
from app.dto.api.response.clubListResponse import ClubListResponse
from app.dto.api.response.departmentListResponse import DepartmentListResponse
from app.dto.api.response.nicknameCheckResponse import NicknameCheckResponse
from app.dto.api.response.userIdCheckResponse import UserIdCheckResponse
from app.dto.api.response.imageUploadResponse import ImageUploadResponse, ImageUploadData
from app.dto.event.response.eventListResponse import EventListResponse
from app.repositories.college_repository import CollegeRepository
from app.repositories.club_repository import ClubRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.services.college_service import CollegeService
from app.services.club_service import ClubService
from app.services.department_service import DepartmentService
from app.services.user_service import UserService
from app.core.settings import get_settings
from app.services.event_service import EventService
from app.repositories.event_repository import EventRepository
from jose import jwt
from fastapi import Header


class ApiService:
    def __init__(self):
        self.college_service = CollegeService(CollegeRepository())
        self.club_service = ClubService(ClubRepository())
        self.department_service = DepartmentService(DepartmentRepository())
        self.user_service = UserService(UserRepository())
        self.settings = get_settings()
        self.event_service = EventService(EventRepository())

    def list_colleges(self, db: Session) -> CollegeListResponse:
        return self.college_service.list_colleges(db)

    def list_clubs(self, db: Session) -> ClubListResponse:
        return self.club_service.list_clubs(db)

    def list_departments(self, db: Session) -> DepartmentListResponse:
        return self.department_service.list_departments(db)

    def check_nickname(self, db: Session, nickname: str) -> NicknameCheckResponse:
        return self.user_service.check_nickname(db, nickname)

    def check_user_id(self, db: Session, user_id: str) -> UserIdCheckResponse:
        return self.user_service.check_user_id(db, user_id)

    async def upload_image(self, file: UploadFile) -> ImageUploadResponse:
        os.makedirs(self.settings.files_dir, exist_ok=True)
        ext = os.path.splitext(file.filename or "")[1].lower() or ".bin"
        filename = f"{uuid.uuid4().hex}{ext}"
        dest_path = os.path.join(self.settings.files_dir, filename)
        with open(dest_path, "wb") as out:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        url = f"{self.settings.files_base_url}/{filename}"
        return ImageUploadResponse(status=200, message="이미지 업로드 성공", data=ImageUploadData(imgUrl=url))

    def list_events(self, db: Session, authorization: str) -> EventListResponse:
        # Expecting header like: "Bearer <token>"
        if not authorization or not authorization.lower().startswith("bearer "):
            return EventListResponse(status=200, message="캘린더 이벤트를 성공적으로 가져왔습니다.", data={"items": []})
        token = authorization.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, self.settings.secret_key, algorithms=[self.settings.jwt_alg])
            user_id = payload.get("sub", "")
        except Exception:
            user_id = ""
        return self.event_service.list_events_for_user(db, user_id)


