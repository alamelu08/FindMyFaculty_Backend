from sqlalchemy import Column, Integer, String
from app.database.database import Base
class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True)
    faculty_code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    cabin = Column(String, nullable=False)
    cabin_directions = Column(String, nullable=True)