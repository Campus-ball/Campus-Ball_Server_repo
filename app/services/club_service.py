from typing import List

from sqlalchemy.orm import Session

from app.dto.api.response.clubListResponse import (
    ClubItem,
    ClubListData,
    ClubListResponse,
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


