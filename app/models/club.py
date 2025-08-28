from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Club(Base):
    __tablename__ = "club"

    club_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    owner_id = Column(
        String(20), ForeignKey("user.user_id"), nullable=False
    )
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    logo_img_url = Column(String(255), nullable=False, default="http://campus-ball-server.kro.kr:30080/files/fdfebbf223f64ff7bfc1d9d6f2e2c456.png")
    chat_url = Column(String(255), nullable=True)
    member_count = Column(Integer, nullable=False, default=11)
    department_id = Column(
        BigInteger, ForeignKey("department.department_id"), nullable=False
    )

    owner = relationship("User", back_populates="owned_clubs", foreign_keys=[owner_id])
    department = relationship("Department", back_populates="clubs")
    members = relationship("User", back_populates="club", foreign_keys="User.club_id")
