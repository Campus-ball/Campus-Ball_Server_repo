from fastapi import APIRouter, Depends, Query, UploadFile, File, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.api.response.departmentListResponse import DepartmentListResponse
from app.dto.api.response.collageListResponse import CollegeListResponse
from app.dto.api.response.clubListResponse import ClubListResponse
from app.dto.api.response.nicknameCheckResponse import NicknameCheckResponse
from app.dto.api.response.imageUploadResponse import ImageUploadResponse
from app.services.api_service import ApiService
from app.dto.api.response.userIdCheckResponse import UserIdCheckResponse


router = APIRouter(prefix="/api", tags=["api"])


@router.get("/department/list", response_model=DepartmentListResponse)
def list_departments(db: Session = Depends(get_db)) -> DepartmentListResponse:
    service = ApiService()
    return service.list_departments(db)


@router.get("/college/list", response_model=CollegeListResponse)
def list_colleges(db: Session = Depends(get_db)) -> CollegeListResponse:
    service = ApiService()
    return service.list_colleges(db)


@router.get("/club/list", response_model=ClubListResponse)
def list_clubs(db: Session = Depends(get_db)) -> ClubListResponse:
    service = ApiService()
    return service.list_clubs(db)


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



