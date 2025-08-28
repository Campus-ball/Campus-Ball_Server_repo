from pydantic import BaseModel


class CreateAvailabilityRequest(BaseModel):
    startDate: str
    startTime: str
    endTime: str
    isRecurring: bool
