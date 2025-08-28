from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from .base import Base


class College(Base):
    __tablename__ = "college"

    college_id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)

    departments = relationship("Department", back_populates="college")
    academic_events = relationship("AcademicEvent", back_populates="college")
