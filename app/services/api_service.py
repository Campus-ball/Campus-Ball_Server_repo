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
from app.repositories.college_repository import CollegeRepository
from app.repositories.club_repository import ClubRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.user_repository import UserRepository
from app.services.college_service import CollegeService
from app.services.club_service import ClubService
from app.services.department_service import DepartmentService
from app.services.user_service import UserService
from app.core.settings import get_settings


class ApiService:
    def __init__(self):
        self.college_service = CollegeService(CollegeRepository())
        self.club_service = ClubService(ClubRepository())
        self.department_service = DepartmentService(DepartmentRepository())
        self.user_service = UserService(UserRepository())
        self.settings = get_settings()

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


