from typing import List

from sqlalchemy.orm import Session

from app.dto.api.response.clubListResponse import (
    ClubItem,
    ClubListData,
    ClubListResponse,
)
from app.dto.club.request.clubInfoResponse import (
    ClubInfoResponse,
    ClubInfoData,
    OpponentInfo,
    CalendarData,
    EventItem,
)
from app.repositories.club_repository import ClubRepository


class ClubService:
    def __init__(self, repository: ClubRepository):
        self.repository = repository

    def list_clubs(self, db: Session) -> ClubListResponse:
        clubs = self.repository.list_all(db)
        items: List[ClubItem] = [
            ClubItem(clubId=int(club.club_id), clubName=club.name) for club in clubs
        ]
        return ClubListResponse(
            status=200,
            message="대학교 조회 성공",
            data=ClubListData(items=items),
        )

    def get_club_info(self, db: Session, my_user_id: str, opponent_club_id: int) -> ClubInfoResponse:
        user, my_club = self.repository.find_user_and_club(db, my_user_id)
        opponent, opp_dept = self.repository.get_opponent_with_department(db, opponent_club_id)

        # opponent block
        opponent_info = OpponentInfo(
            clubId=int(opponent.club_id) if opponent else 0,
            clubName=opponent.name if opponent else "",
            departmentName=(f"{opp_dept.college.name} {opp_dept.name}" if opp_dept else ""),
            clubLogoUrl=(opponent.logo_img_url if opponent else None),
            clubDescription=(opponent.description if opponent else None),
        )

        def build_calendar_items_for_club(club) -> List[EventItem]:
            if not club:
                return []
            items: List[EventItem] = []
            # academic
            for ev in self.repository.list_academic_events_by_club(db, club):
                items.append(
                    EventItem(
                        eventId=int(ev.event_id),
                        eventType="ACADEMIC",
                        title=ev.title,
                        startDate=ev.start_date.isoformat(),
                        endDate=ev.end_date.isoformat(),
                        startTime="00:00",
                        endTime="23:59",
                    )
                )
            # availability
            for av in self.repository.list_availability_by_club(db, club.club_id):
                items.append(
                    EventItem(
                        eventId=int(av.availability_id),
                        eventType="AVAILABILITY",
                        title="경기 가용 시간",
                        startDate=(av.start_date.isoformat() if av.start_date else ""),
                        endDate=(av.end_date.isoformat() if av.end_date else (av.start_date.isoformat() if av.start_date else "")),
                        startTime=(av.start_time.strftime("%H:%M") if av.start_time else "00:00"),
                        endTime=(av.end_time.strftime("%H:%M") if av.end_time else (av.start_time.strftime("%H:%M") if av.start_time else "00:00")),
                    )
                )
            # match
            for m in self.repository.list_matches_by_club(db, club.club_id):
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
            return items

        my_items = build_calendar_items_for_club(my_club)
        opp_items = build_calendar_items_for_club(opponent)

        return ClubInfoResponse(
            status=200,
            message="성공",
            data=ClubInfoData(
                opponent=opponent_info,
                myCalendar=CalendarData(items=my_items),
                opponentCalendar=CalendarData(items=opp_items),
            ),
        )


