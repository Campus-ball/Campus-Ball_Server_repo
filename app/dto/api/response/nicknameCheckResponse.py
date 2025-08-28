from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class NicknameCheckData(BaseModel):
    isValid: bool


class NicknameCheckResponse(BaseResponse[NicknameCheckData]):
    pass


