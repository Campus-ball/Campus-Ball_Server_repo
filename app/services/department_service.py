from typing import List

from sqlalchemy.orm import Session

from app.dto.api.response.departmentListResponse import (
    DepartmentItem,
    DepartmentListData,
    DepartmentListResponse,
)
from app.repositories.department_repository import DepartmentRepository


class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    def list_departments(self, db: Session) -> DepartmentListResponse:
        departments = self.repository.list_all(db)
        items: List[DepartmentItem] = [
            DepartmentItem(
                departmentId=int(dept.department_id),
                departmentName=dept.name,
            )
            for dept in departments
        ]
        return DepartmentListResponse(
            status=200,
            message="학과 조회 성공",
            data=DepartmentListData(items=items),
        )
