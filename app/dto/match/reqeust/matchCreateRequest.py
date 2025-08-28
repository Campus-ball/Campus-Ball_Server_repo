from pydantic import BaseModel, Field


class MatchCreateRequest(BaseModel):
    clubId: int = Field(alias="cludId")
