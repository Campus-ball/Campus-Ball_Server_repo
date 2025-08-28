from typing import List

from sqlalchemy.orm import Session

from app.dto.api.response.collageListResponse import (
    CollegeItem,
    CollegeListData,
    CollegeListResponse,
)
from app.repositories.college_repository import CollegeRepository


class CollegeService:
    def __init__(self, repository: CollegeRepository):
        self.repository = repository

    def list_colleges(self, db: Session) -> CollegeListResponse:
        colleges = self.repository.list_all(db)
        items: List[CollegeItem] = [
            CollegeItem(collegeId=int(col.college_id), collegeName=col.name)
            for col in colleges
        ]
        return CollegeListResponse(
            status=200,
            message="대학교 조회 성공",
            data=CollegeListData(items=items),
        )


