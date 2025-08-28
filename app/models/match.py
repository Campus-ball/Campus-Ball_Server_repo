from sqlalchemy import BigInteger, Column, Date, ForeignKeyConstraint, String, Time
from sqlalchemy.orm import relationship

from .base import Base


class Match(Base):
    __tablename__ = "match"

    match_id = Column(BigInteger, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True)
    type = Column(String(20), nullable=False, default="친선 경기")
    club_id = Column(BigInteger, nullable=False)
    owner_id = Column(String(20), nullable=False)
    club_id2 = Column(BigInteger, nullable=False)
    owner_id2 = Column(String(20), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["club_id", "owner_id"], ["club.club_id", "club.owner_id"]
        ),
        ForeignKeyConstraint(
            ["club_id2", "owner_id2"], ["club.club_id", "club.owner_id"]
        ),
    )

    home_club = relationship("Club", foreign_keys=[club_id, owner_id])
    away_club = relationship("Club", foreign_keys=[club_id2, owner_id2])
