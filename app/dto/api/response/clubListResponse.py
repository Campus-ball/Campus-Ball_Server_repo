from typing import List

from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class ClubItem(BaseModel):
    clubId: int
    clubName: str


class ClubListData(BaseModel):
    items: List[ClubItem]


class ClubListResponse(BaseResponse[ClubListData]):
    pass


