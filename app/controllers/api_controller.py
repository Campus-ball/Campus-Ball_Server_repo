from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dto.api.response.departmentListResponse import DepartmentListResponse
from app.repositories.department_repository import DepartmentRepository
from app.services.department_service import DepartmentService


router = APIRouter(prefix="/api", tags=["api"])


@router.get("/department/list", response_model=DepartmentListResponse)
def list_departments(db: Session = Depends(get_db)) -> DepartmentListResponse:
    service = DepartmentService(DepartmentRepository())
    return service.list_departments(db)
