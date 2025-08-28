from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class TokenPair(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str = "bearer"


class LoginResponse(BaseResponse[TokenPair]):
    pass
