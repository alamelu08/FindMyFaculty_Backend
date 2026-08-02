from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyCreate, FacultyUpdate
from datetime import datetime
from app.models.faculty_timetable import FacultyTimetable
from app.models.period import Period
from datetime import time


def create_faculty(db: Session, faculty: FacultyCreate):
    new_faculty = Faculty(
        name=faculty.name,
        image_url=faculty.image_url,
        cabin=faculty.cabin,
        cabin_directions=faculty.cabin_directions
    )
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    return new_faculty

def get_all_faculties(db: Session):
    return db.query(Faculty).all()

def get_faculty_by_id(db: Session, faculty_id: int):
    return db.query(Faculty).filter(Faculty.id == faculty_id).first()

def update_faculty(db: Session, faculty_id: int, faculty: FacultyUpdate):
    existing_faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not existing_faculty:
        return None
    existing_faculty.name = faculty.name
    existing_faculty.image_url = faculty.image_url
    existing_faculty.cabin = faculty.cabin
    existing_faculty.cabin_directions = faculty.cabin_directions
    db.commit()
    db.refresh(existing_faculty)
    return existing_faculty

def delete_faculty(db: Session, faculty_id: int):
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        return None
    db.delete(faculty)
    db.commit()
    return faculty

def search_faculty(db: Session, name: str):
    return db.query(Faculty).filter(
        Faculty.name.ilike(f"%{name}%")
    ).all()   

def get_faculty_details(faculty_code: str, db: Session):

    faculty = (
        db.query(Faculty)
        .filter(Faculty.faculty_code == faculty_code)
        .first()
    )

    if faculty is None:
        return {"message": "Faculty not found"}

    current_day = get_current_day()
    current_period = get_current_period(db)
    if current_day in ["SUN"]:
        return {
            "faculty": faculty.name,
            "status": "Holiday",
            "location": faculty.cabin,
            "message": f"Today is {current_day}"
        }
    # Outside college hours
    if current_period is None:
        return {
            "faculty": faculty.name,
            "status": "Available",
            "location": faculty.cabin,
            "message": "Outside working hours"
        }

    timetable = (
        db.query(FacultyTimetable)
        .filter(
            FacultyTimetable.faculty_id == faculty.id,
            FacultyTimetable.day == current_day,
            FacultyTimetable.period_no == current_period
        )
        .first()
    )

    if timetable:
        return {
            "faculty": faculty.name,
            "status": "In Class",
            "location": timetable.room,
            "day": current_day,
            "period": current_period
        }

    return {
        "faculty": faculty.name,
        "status": "Available",
        "location": faculty.cabin,
        "day": current_day,
        "period": current_period
    }
from datetime import datetime
from app.models.faculty import Faculty
from app.models.faculty_timetable import FacultyTimetable
from app.models.period import Period


def get_faculty_location(db, faculty_id: int):

    faculty = (
        db.query(Faculty)
        .filter(Faculty.id == faculty_id)
        .first()
    )

    if not faculty:
        return None

    # Current day
    current_day = get_current_day()
    current_period = get_current_period(db)
    # Find current period
    current_period = (
        db.query(Period)
        .filter(
            Period.start_time <= current_time,
            Period.end_time >= current_time
        )
        .first()
    )

    if not current_period:
        return {
            "faculty": faculty.name,
            "status": "Free",
            "location": faculty.cabin,
            "day": current_day,
            "period": None
        }

    timetable = (
        db.query(FacultyTimetable)
        .filter(
            FacultyTimetable.faculty_id == faculty.id,
            FacultyTimetable.day == current_day,
            FacultyTimetable.period_no == current_period.period_no
        )
        .first()
    )

    if timetable:
        return {
            "faculty": faculty.name,
            "status": "In Class",
            "location": timetable.room,
            "day": current_day,
            "period": current_period.period_no
        }

    return {
        "faculty": faculty.name,
        "status": "Available",
        "location": faculty.cabin,
        "day": current_day,
        "period": current_period.period_no
    }
def get_current_period(db: Session):
    current_time = datetime.now().time()

    periods = db.query(Period).all()

    for period in periods:
        if period.start_time <= current_time <= period.end_time:
            return period.period_no

    return None
def get_current_day():
    return datetime.now().strftime("%a").upper()
