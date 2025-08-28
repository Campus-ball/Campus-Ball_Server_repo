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
