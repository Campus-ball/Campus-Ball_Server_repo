from datetime import date, time
from typing import List

from sqlalchemy.orm import Session

from app.dto.event.response.eventListResponse import (
    EventItem,
    EventListData,
    EventListResponse,
)
from app.repositories.event_repository import EventRepository
from app.models import Department


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def list_events_for_user(self, db: Session, user_id: str) -> EventListResponse:
        user, club = self.repository.find_user_and_club(db, user_id)
        if user is None or club is None:
            return EventListResponse(status=404, message="엔티티가 존재하지 않습니다.", data=EventListData(items=[]))

        # Determine college via department
        department = db.query(Department).filter(Department.department_id == club.department_id).first()
        college_id = department.college_id if department else None

        items: List[EventItem] = []

        # Academic events (by college)
        if college_id is not None:
            academic_events = self.repository.list_academic_events_by_college(db, college_id)
            for ev in academic_events:
                items.append(
                    EventItem(
                        eventId=int(ev.event_id),
                        eventType="ACADEMIC",
                        title=ev.title,
                        startDate=ev.start_date.isoformat(),
                        endDate=ev.end_date.isoformat(),
                        startTime="00:00",  # Academic events don't have time, use default
                        endTime="23:59",    # Academic events don't have time, use default
                    )
                )

        # Availability events (by club)
        availabilities = self.repository.list_availability_by_club(db, club.club_id)
        for av in availabilities:
            start_date = av.start_date.isoformat() if av.start_date else ""
            end_date = av.end_date.isoformat() if av.end_date else start_date
            start_time = av.start_time.strftime("%H:%M") if av.start_time else "00:00"
            end_time = av.end_time.strftime("%H:%M") if av.end_time else start_time
            items.append(
                EventItem(
                    eventId=int(av.availability_id),
                    eventType="AVAILABILITY",
                    title="경기 가용 시간",
                    startDate=start_date,
                    endDate=end_date,
                    startTime=start_time,
                    endTime=end_time,
                )
            )

        # Match events (by club)
        matches = self.repository.list_matches_by_club(db, club.club_id)
        for m in matches:
            items.append(
                EventItem(
                    eventId=int(m.match_id),
                    eventType="MATCH",
                    title=m.type,
                    startDate=m.date.isoformat(),
                    endDate=m.date.isoformat(),
                    startTime=m.start_time.strftime("%H:%M"),
                    endTime=(m.end_time.strftime("%H:%M") if m.end_time else m.start_time.strftime("%H:%M")),
                )
            )

        return EventListResponse(
            status=200,
            message="캘린더 이벤트를 성공적으로 가져왔습니다.",
            data=EventListData(items=items),
        )


