from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class AccessTokenData(BaseModel):
    accessToken: str
    tokenType: str = "Bearer"


class RefreshTokenResponse(BaseResponse[AccessTokenData]):
    pass
