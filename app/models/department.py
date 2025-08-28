from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class Department(Base):
    __tablename__ = "department"

    department_id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    college_id = Column(BigInteger, ForeignKey("college.college_id"), nullable=False)

    college = relationship("College", back_populates="departments")
    clubs = relationship("Club", back_populates="department")
