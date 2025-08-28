from fastapi import APIRouter, Depends, Query, UploadFile, File, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.api.response.departmentListResponse import DepartmentListResponse
from app.repositories.department_repository import DepartmentRepository
from app.services.department_service import DepartmentService
from app.dto.api.response.collageListResponse import CollegeListResponse
from app.dto.api.response.clubListResponse import ClubListResponse
from app.dto.api.response.nicknameCheckResponse import NicknameCheckResponse
from app.dto.api.response.imageUploadResponse import ImageUploadResponse
from app.services.api_service import ApiService
from app.services.club_service import ClubService
from app.repositories.club_repository import ClubRepository
from app.dto.api.response.userIdCheckResponse import UserIdCheckResponse


router = APIRouter(prefix="/api", tags=["api"])


@router.get("/department/{college_id}/list", response_model=DepartmentListResponse)
def list_departments(college_id: int, db: Session = Depends(get_db)) -> DepartmentListResponse:
    service = DepartmentService(DepartmentRepository())
    return service.list_departments(db, college_id)


@router.get("/college/list", response_model=CollegeListResponse)
def list_colleges(db: Session = Depends(get_db)) -> CollegeListResponse:
    service = ApiService()
    return service.list_colleges(db)


@router.get("/club/{department_id}/list", response_model=ClubListResponse)
def list_clubs(department_id: int, db: Session = Depends(get_db)) -> ClubListResponse:
    service = ClubService(ClubRepository())
    return service.list_clubs_by_department(db, department_id)


@router.get("/nickname/check", response_model=NicknameCheckResponse)
def nickname_check(q: str = Query(""), db: Session = Depends(get_db)) -> NicknameCheckResponse:
    service = ApiService()
    return service.check_nickname(db, q)


@router.get("/userid/check", response_model=UserIdCheckResponse)
def userid_check(q: str = Query(""), db: Session = Depends(get_db)) -> UserIdCheckResponse:
    service = ApiService()
    return service.check_user_id(db, q)


@router.post("/images/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)) -> ImageUploadResponse:
    service = ApiService()
    return await service.upload_image(file)



