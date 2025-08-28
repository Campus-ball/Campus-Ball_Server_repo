from sqlalchemy import BigInteger, Column, Date, ForeignKey, String, Time
from sqlalchemy.orm import relationship

from .base import Base


class Availability(Base):
    __tablename__ = "availability"

    availability_id = Column(BigInteger, primary_key=True, nullable=False)
    start_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)
    end_date = Column(Date, nullable=True)
    end_time = Column(Time, nullable=True)
    club_id = Column(BigInteger, ForeignKey("club.club_id"), nullable=False)
    owner_id = Column(String(100), nullable=False)

    club = relationship("Club")
