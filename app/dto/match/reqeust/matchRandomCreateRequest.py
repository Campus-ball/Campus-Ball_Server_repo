from pydantic import BaseModel


class MatchRandomCreateRequest(BaseModel):
    clubId: int
    startDate: str
    startTime: str
