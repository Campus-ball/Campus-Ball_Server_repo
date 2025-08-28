from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class CreateAvailabilityData(BaseModel):
    availabilityId: int


class CreateAvailabilityResponse(BaseResponse[CreateAvailabilityData]):
    pass
