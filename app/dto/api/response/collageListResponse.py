from typing import List

from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class CollegeItem(BaseModel):
    collegeId: int
    collegeName: str


class CollegeListData(BaseModel):
    items: List[CollegeItem]


class CollegeListResponse(BaseResponse[CollegeListData]):
    pass


