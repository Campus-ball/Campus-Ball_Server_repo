from sqlalchemy import BigInteger, Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class AcademicEvent(Base):
    __tablename__ = "academic_events"

    event_id = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    college_id = Column(BigInteger, ForeignKey("college.college_id"), nullable=False)

    college = relationship("College", back_populates="academic_events")
