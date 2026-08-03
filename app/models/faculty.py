from sqlalchemy import Column, String
from app.database.database import Base
class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(String, primary_key=True, index=True)   # F01, F02, ...
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    cabin = Column(String, nullable=False)
    cabin_directions = Column(String, nullable=True)