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

        # 1. 현재 클럽의 가용시간 조회
        my_availabilities = self.repository.find_my_availabilities(db, club.club_id)
        if not my_availabilities:
            return MatchRandomResponse(
                status=500,
                message="등록된 가용시간이 없습니다. 먼저 가용시간을 등록해주세요.",
                data=None,
            )

        # 2. 각 가용시간별로 매칭 가능한 상대 찾기
        candidates = []
        for my_avail in my_availabilities:
            # 같은 날짜에 가용시간이 있는 다른 클럽들 찾기
            matching_clubs = self.repository.find_clubs_with_matching_availability(
                db,
                club.club_id,
                my_avail.start_date,
                my_avail.start_time,
                my_avail.end_time,
            )

            for candidate_club, candidate_avail, match_count in matching_clubs:
                # 시간 겹침 검사
                if self._time_overlaps(my_avail, candidate_avail):
                    candidates.append(
                        {
                            "club": candidate_club,
                            "availability": candidate_avail,
                            "my_availability": my_avail,
                            "match_count": match_count or 0,
                        }
                    )

        if not candidates:
            return MatchRandomResponse(
                status=500,
                message="매칭 가능한 상대를 찾지 못했습니다. 다른 날짜의 가용시간을 등록해보세요.",
                data=None,
            )

        # 3. 점수화 및 선택
        from math import exp
        import random

        # 점수: 최근 경기 수가 적을수록 높게 (-cnt)
        def score(candidate):
            return -float(candidate["match_count"])

        # Top-K 선택
        candidates.sort(key=lambda x: score(x))
        top_k = candidates[: min(5, len(candidates))]

        # 소프트맥스 가중 랜덤 선택
        tau = 0.6  # temperature
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

        candidate_club = chosen["club"]
        candidate_avail = chosen["availability"]

        # 4. 응답 데이터 구성
        slot_date = (
            candidate_avail.start_date.isoformat() if candidate_avail.start_date else ""
        )
        slot_time = (
            candidate_avail.start_time.strftime("%H:%M")
            if candidate_avail.start_time
            else ""
        )

        # 관계 사용(직접 쿼리 대신)
        dept = candidate_club.department
        dept_name = (
            f"{dept.college.name} {dept.name}"
            if dept and getattr(dept, "college", None)
            else ""
        )

        return MatchRandomResponse(
            status=200,
            message="매칭된 상대방 정보를 성공적으로 가져왔습니다.",
            data=MatchRandomData(
                clubId=int(candidate_club.club_id),
                clubName=candidate_club.name,
                departmentName=dept_name,
                clubLogoUrl=candidate_club.logo_img_url,
                clubDescription=candidate_club.description,
                startDate=slot_date or "",
                startTime=slot_time or "",
            ),
        )

    def _time_overlaps(self, avail1, avail2) -> bool:
        """두 가용시간이 겹치는지 확인"""
        if (
            avail1.start_time <= avail2.end_time
            and avail2.start_time <= avail1.end_time
        ):
            return True
        return False

    def random_request(
        self, db: Session, user_id: str, body: MatchRandomCreateRequest
    ) -> MatchRandomCreateResponse:
        # startTime으로부터 1시간 뒤를 endTime으로 자동 계산
        from datetime import datetime, timedelta

        start_time = datetime.strptime(body.startTime, "%H:%M").time()
        end_time = (
            datetime.combine(datetime.today(), start_time) + timedelta(hours=1)
        ).time()
        end_time_str = end_time.strftime("%H:%M")

        request_id = self.repository.create_random_request(
            db,
            from_user_id=user_id,
            target_club_id=int(body.clubId),
            start_date=body.startDate,
            start_time=body.startTime,
            end_time=end_time_str,
        )
        db.commit()
        return MatchRandomCreateResponse(
            status=200,
            message="친선 경기 신청에 성공하였습니다!",
            data=MatchRandomCreateData(requestId=int(request_id)),
        )
