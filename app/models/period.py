from sqlalchemy import Column, Integer, Time
from app.database.database import Base
class Period(Base):
    __tablename__ = "period"
    period_no = Column(Integer, primary_key=True, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)