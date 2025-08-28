from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class MatchRandomCreateData(BaseModel):
    requestId: int


class MatchRandomCreateResponse(BaseResponse[MatchRandomCreateData]):
    pass
