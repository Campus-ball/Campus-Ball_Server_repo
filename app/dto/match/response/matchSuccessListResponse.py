from typing import List
from pydantic import BaseModel
from app.dto.baseResponse import BaseResponse


class MatchSuccessListItem(BaseModel):
    matchId: int
    matchType: str
    clubId: int
    clubName: str
    departmentName: str
    clubLogoUrl: str | None = None
    chatUrl: str | None = None


class MatchSuccessListData(BaseModel):
    items: List[MatchSuccessListItem]


class MatchSuccessListResponse(BaseResponse[MatchSuccessListData]):
    pass
