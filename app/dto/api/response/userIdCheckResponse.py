from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class UserIdCheckData(BaseModel):
    isValid: bool


class UserIdCheckResponse(BaseResponse[UserIdCheckData]):
    pass


