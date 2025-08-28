from sqlalchemy.orm import Session

from app.dto.match.response.matchAcceptResponse import MatchAcceptResponse
from app.dto.match.response.matchRejectResponse import MatchRejectResponse
from app.dto.match.reqeust.matchAcceptRequest import MatchAcceptRequest
from app.repositories.match_repository import MatchRepository
from app.dto.match.response.matchListResponse import (
    MatchListItem,
    MatchListData,
    MatchListResponse,
)
from app.dto.match.response.matchSuccessListResponse import (
    MatchSuccessListItem,
    MatchSuccessListData,
    MatchSuccessListResponse,
)
from app.dto.match.reqeust.matchCreateRequest import MatchCreateRequest
from app.dto.match.response.matchCreateResponse import MatchCreateResponse
from app.dto.match.response.matchRandomResponse import (
    MatchRandomResponse,
    MatchRandomData,
)
from app.models import Department


class MatchService:
    def __init__(self, repository: MatchRepository):
        self.repository = repository

    def accept_match(
        self, db: Session, body: MatchAcceptRequest
    ) -> MatchAcceptResponse:
        req, club1, club2 = self.repository.get_request_with_clubs(
            db, int(body.requestId)
        )
        if req is None or club1 is None or club2 is None:
            return MatchAcceptResponse(
                status=500, message="제안을 수락하는데 실패했습니다.", data=None
            )
        self.repository.create_match_from_request(db, req)
        self.repository.delete_request(db, req)
        db.commit()
        return MatchAcceptResponse(
            status=200, message="제안을 수락했습니다.", data=None
        )

    def reject_match(
        self, db: Session, body: MatchAcceptRequest
    ) -> MatchRejectResponse:
        req = self.repository.get_request_by_id(db, int(body.requestId))
        if req is None:
            return MatchRejectResponse(
                status=500, message="제안을 거절하는데 실패했습니다.", data=None
            )
        self.repository.delete_request(db, req)
        db.commit()
        return MatchRejectResponse(
            status=200, message="제안을 거절했습니다.", data=None
        )

    def list_received_requests(self, db: Session, user_id: str) -> MatchListResponse:
        user, club = self.repository.find_user_and_club(db, user_id)
        if not user or not club:
            return MatchListResponse(
                status=500, message="동아리 가져오기 실패", data=MatchListData(items=[])
            )
        rows = self.repository.list_received_requests(db, club.club_id)
        items = [
            MatchListItem(
                requestId=int(req.request_id),
                requestType=req.type,
                clubId=int(c.club_id),
                clubName=c.name,
                departmentName=f"{dept.college.name} {dept.name}",
                clubLogoUrl=c.logo_img_url,
            )
            for (req, c, dept) in rows
        ]
        return MatchListResponse(
            status=200,
            message="받은 신청 목록을 성공적으로 가져왔습니다.",
            data=MatchListData(items=items),
        )

    def list_success_matches(
        self, db: Session, user_id: str
    ) -> MatchSuccessListResponse:
        user, club = self.repository.find_user_and_club(db, user_id)
        if not user or not club:
            return MatchSuccessListResponse(
                status=500,
                message="동아리 가져오기 실패",
                data=MatchSuccessListData(items=[]),
            )
        rows = self.repository.list_success_matches(db, club.club_id)
        items = [
            MatchSuccessListItem(
                matchId=int(m.match_id),
                matchType=m.type,
                clubId=int(c.club_id),
                clubName=c.name,
                departmentName=f"{dept.college.name} {dept.name}",
                clubLogoUrl=c.logo_img_url,
                chatUrl=c.chat_url,
            )
            for (m, c, dept) in rows
        ]
        return MatchSuccessListResponse(
            status=200,
            message="성사된 경기 목록을 성공적으로 가져왔습니다.",
            data=MatchSuccessListData(items=items),
        )

    def create_friendly_request(
        self, db: Session, user_id: str, body: MatchCreateRequest
    ) -> MatchCreateResponse:
        self.repository.create_friendly_request(db, user_id, int(body.clubId))
        db.commit()
        return MatchCreateResponse(status=200, message="상대를 찾았습니다!", data=None)

    def random_opponent(self, db: Session, user_id: str) -> MatchRandomResponse:
        user, club = self.repository.find_user_and_club(db, user_id)
        if not user or not club:
            return MatchRandomResponse(
                status=500, message="동아리 가져오기 실패", data=None
            )
        # Two-join strategy
        by_match = self.repository.find_candidate_clubs_by_match(db, club.club_id)
        by_avail = self.repository.find_candidate_slots_by_availability(
            db, club.club_id
        )
        # Choose first club that appears in availability list
        # 나중에 알고리즘 적용할 부분
        candidate = None
        slot_date = None
        slot_time = None
        avail_map = {}
        for c, a in by_avail:
            if c.club_id not in avail_map:
                avail_map[c.club_id] = a
        for c, _cnt in by_match:
            a = avail_map.get(c.club_id)
            if a is not None:
                candidate = c
                slot_date = a.start_date.isoformat() if a.start_date else ""
                slot_time = a.start_time.strftime("%H:%M") if a.start_time else ""
                break
        if candidate is None:
            return MatchRandomResponse(
                status=500,
                message="매칭된 상대를 찾지 못했습니다.",
                data=None,
            )
        dept = (
            db.query(Department)
            .filter(Department.department_id == candidate.department_id)
            .first()
        )
        dept_name = f"{dept.college.name} {dept.name}" if dept and dept.college else ""
        return MatchRandomResponse(
            status=200,
            message="매칭된 상대방 정보를 성공적으로 가져왔습니다.",
            data=MatchRandomData(
                clubId=int(candidate.club_id),
                clubName=candidate.name,
                departmentName=dept_name,
                clubLogoUrl=candidate.logo_img_url,
                clubDescription=candidate.description,
                startDate=slot_date or "",
                startTime=slot_time or "",
            ),
        )
