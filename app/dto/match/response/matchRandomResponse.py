from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class MatchRandomData(BaseModel):
    clubId: int
    clubName: str
    departmentName: str
    clubLogoUrl: str | None = None
    clubDescription: str
    startDate: str
    startTime: str


class MatchRandomResponse(BaseResponse[MatchRandomData]):
    pass
