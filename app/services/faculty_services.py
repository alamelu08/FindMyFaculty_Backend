from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyCreate, FacultyUpdate
from datetime import datetime
from app.models.faculty_timetable import FacultyTimetable
from app.models.period import Period
from datetime import time
from app.utils.uuid_generator import generate_faculty_uuid
from app.utils.image_finder import find_image_url
from app.utils.name_normalizer import normalize_name


def create_faculty(db: Session, faculty: FacultyCreate):

    normalized_name = normalize_name(faculty.name)

    new_faculty = Faculty(
        id=generate_faculty_uuid(normalized_name),
        name=normalized_name,
        image_url=find_image_url(normalized_name),
        cabin=faculty.cabin,
        cabin_directions=faculty.cabin_directions
    )

    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)

    return new_faculty

def get_all_faculties(db: Session):
    return db.query(Faculty).all()

def get_faculty_by_id(db: Session, faculty_id: str):
    return db.query(Faculty).filter(Faculty.id == faculty_id).first()

def update_faculty(db: Session, faculty_name: str, faculty: FacultyUpdate):

    existing_faculty = (
        db.query(Faculty)
        .filter(Faculty.name == normalize_name(faculty_name))
        .first()
    )

    if not existing_faculty:
        return None

    normalized_name = normalize_name(faculty.name)

    existing_faculty.name = normalized_name
    existing_faculty.image_url = find_image_url(normalized_name)
    existing_faculty.cabin = faculty.cabin
    existing_faculty.cabin_directions = faculty.cabin_directions

    db.commit()
    db.refresh(existing_faculty)

    return existing_faculty

def delete_faculty(db: Session, faculty_name: str):
    faculty = (
        db.query(Faculty)
        .filter(Faculty.name == faculty_name)
        .first()
    )
    if not faculty:
        return None
    db.delete(faculty)
    db.commit()
    return faculty

def search_faculty(db: Session, name: str):
    return db.query(Faculty).filter(
        Faculty.name.ilike(f"%{name}%")
    ).all()   

def get_faculty_details(faculty_id: str, db: Session):

    faculty = (
        db.query(Faculty)
        .filter(Faculty.id == faculty_id)
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



def get_faculty_location(db, faculty_id: str):

    faculty = (
        db.query(Faculty)
        .filter(Faculty.id == faculty_id)
        .first()
    )

    if not faculty:
        return None

    # Current day
    current_day = get_current_day()
    current_time = datetime.now().time()
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
            "location": faculty.cabin,
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
            "location": timetable.room
    }

    return {
        "location": faculty.cabin
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
