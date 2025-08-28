from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(String(20), primary_key=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
    name = Column(String(50), nullable=False)
    nickname = Column(String(30), nullable=False)
    phone_number = Column(String(20), nullable=False)
    gender = Column(String(10), nullable=False)
    role = Column(String(10), nullable=False, default="MEMBER")
    club_id = Column(BigInteger, ForeignKey("club.club_id"), nullable=False)

    owned_clubs = relationship(
        "Club", back_populates="owner", foreign_keys="Club.owner_id"
    )
    club = relationship("Club", back_populates="members", foreign_keys=[club_id])
