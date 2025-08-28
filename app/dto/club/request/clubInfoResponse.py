from typing import List, Optional

from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class OpponentInfo(BaseModel):
    clubId: int
    clubName: str
    departmentName: str
    clubLogoUrl: Optional[str] = None
    clubDescription: Optional[str] = None


class EventItem(BaseModel):
    eventId: int
    eventType: str
    title: str
    startDate: str
    endDate: str
    startTime: str
    endTime: str


class CalendarData(BaseModel):
    items: List[EventItem]


class ClubInfoData(BaseModel):
    opponent: OpponentInfo
    myCalendar: CalendarData
    opponentCalendar: CalendarData


class ClubInfoResponse(BaseResponse[ClubInfoData]):
    pass


