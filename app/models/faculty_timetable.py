from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class FacultyTimetable(Base):
    __tablename__ = "faculty_timetable"
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=False)
    day = Column(String, nullable=False)
    period_no = Column(Integer, ForeignKey("period.period_no"), nullable=False)
    room = Column(String, nullable=False)
    faculty = relationship("Faculty")
    period = relationship("Period")