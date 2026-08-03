from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyCreate, FacultyUpdate
from datetime import datetime
from app.models.faculty_timetable import FacultyTimetable
from app.models.period import Period

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




