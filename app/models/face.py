from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from ..database import Base


class FaceCapture(Base):
    __tablename__ = "face_data"

    id = Column(Integer(), primary_key=True, index=True)
    device_id = Column(String(255), index=True, unique=False, nullable=False)
    face_id = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=False)
