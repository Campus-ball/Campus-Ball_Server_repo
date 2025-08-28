from typing import List

from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class MatchListItem(BaseModel):
    requestId: int
    requestType: str
    clubId: int
    clubName: str
    departmentName: str
    clubLogoUrl: str | None = None


class MatchListData(BaseModel):
    items: List[MatchListItem]


class MatchListResponse(BaseResponse[MatchListData]):
    pass


