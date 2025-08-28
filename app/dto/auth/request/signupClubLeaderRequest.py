from pydantic import BaseModel, Field


class SignUpClubLeaderRequest(BaseModel):
    name: str
    nickname: str
    gender: str
    userId: str = Field(alias="userId")
    password: str
    clubName: str
    clubDescription: str
    collegeId: int
    departmentId: int
    phoneNumber: str
    clubLogoUrl: str | None = None
    chatUrl: str | None = None
