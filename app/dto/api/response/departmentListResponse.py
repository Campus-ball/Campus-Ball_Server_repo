from typing import List

from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class DepartmentItem(BaseModel):
    departmentId: int
    departmentName: str


class DepartmentListData(BaseModel):
    items: List[DepartmentItem]


class DepartmentListResponse(BaseResponse[DepartmentListData]):
    pass
