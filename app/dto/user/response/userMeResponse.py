from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class UserMeData(BaseModel):
    name: str
    nickname: str
    gender: str
    clubName: str | None = None
    phoneNumber: str
    chatUrl: str | None = None


class UserMeResponse(BaseResponse[UserMeData]):
    pass
