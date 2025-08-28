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
from app.dto.match.reqeust.matchRandomCreateRequest import MatchRandomCreateRequest
from app.dto.match.response.matchRandomCreateResponse import (
    MatchRandomCreateResponse,
    MatchRandomCreateData,
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
        # Two-join strategy: 후보 수집
        by_match = self.repository.find_candidate_clubs_by_match(db, club.club_id)
        by_avail = self.repository.find_candidate_slots_by_availability(
            db, club.club_id
        )

        # club_id -> earliest availability
        avail_map = {}
        for c, a in by_avail:
            if c.club_id not in avail_map:
                avail_map[c.club_id] = a

        # 점수화: 최근 경기 수가 적은 순, 가장 이른 슬롯 우선, tie-breaker club_id
        candidates = []
        for c, cnt in by_match:
            a = avail_map.get(c.club_id)
            if a is None:
                continue
            date_key = a.start_date.isoformat() if a.start_date else "9999-12-31"
            time_key = a.start_time.strftime("%H:%M") if a.start_time else "23:59"
            candidates.append((cnt or 0, date_key, time_key, int(c.club_id), c, a))

        if not candidates:
            return MatchRandomResponse(
                status=500,
                message="매칭된 상대를 찾지 못했습니다.",
                data=None,
            )

        # Top-K -> 소프트맥스 가중 랜덤 선택으로 다양성 확보
        from math import exp
        import random

        candidates.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
        top_k = candidates[: min(5, len(candidates))]

        # 점수: 최근 경기 수가 적을수록 높게 (-cnt), 더 이른 슬롯에 작은 패널티
        def score(item):
            cnt, d, t, _cid, _c, _a = item
            # 날짜/시간 패널티(가벼운 영향)
            date_penalty = 0.0 if d == "" else 0.001
            time_penalty = 0.0 if t == "" else 0.001
            return -float(cnt) - date_penalty - time_penalty

        tau = 0.6  # temperature: 낮을수록 상위 편향, 높을수록 다양성↑
        scores = [score(it) for it in top_k]
        exps = [exp(s / tau) for s in scores]
        ssum = sum(exps) or 1.0
        probs = [v / ssum for v in exps]

        r = random.random()
        acc = 0.0
        chosen = top_k[0]
        for it, p in zip(top_k, probs):
            acc += p
            if r <= acc:
                chosen = it
                break

        _cnt, _d, _t, _cid, candidate, a = chosen
        slot_date = a.start_date.isoformat() if a.start_date else ""
        slot_time = a.start_time.strftime("%H:%M") if a.start_time else ""
        if candidate is None:
            return MatchRandomResponse(
                status=500,
                message="매칭된 상대를 찾지 못했습니다.",
                data=None,
            )
        # 관계 사용(직접 쿼리 대신)
        dept = candidate.department
        dept_name = (
            f"{dept.college.name} {dept.name}"
            if dept and getattr(dept, "college", None)
            else ""
        )
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

    def random_request(
        self, db: Session, user_id: str, body: MatchRandomCreateRequest
    ) -> MatchRandomCreateResponse:
        request_id = self.repository.create_random_request(
            db,
            from_user_id=user_id,
            target_club_id=int(body.clubId),
            start_date=body.startDate,
            start_time=body.startTime,
        )
        db.commit()
        return MatchRandomCreateResponse(
            status=200,
            message="친선 경기 신청에 성공하였습니다!",
            data=MatchRandomCreateData(requestId=int(request_id)),
        )
