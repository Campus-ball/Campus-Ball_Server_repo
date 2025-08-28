from pydantic import BaseModel


class MatchAcceptRequest(BaseModel):
    requestId: int


