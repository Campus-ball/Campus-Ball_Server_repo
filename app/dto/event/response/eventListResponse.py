from typing import List

from pydantic import BaseModel

from app.dto.baseResponse import BaseResponse


class EventItem(BaseModel):
    eventId: int
    eventType: str
    title: str
    startDate: str
    endDate: str
    startTime: str
    endTime: str


class EventListData(BaseModel):
    items: List[EventItem]


class EventListResponse(BaseResponse[EventListData]):
    pass


