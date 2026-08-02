from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.faculty import FacultyResponse
from app.services.faculty_services import (
    get_all_faculties,
    get_faculty_by_id,
    search_faculty,
    get_faculty_location,
    get_faculty_details
)
router = APIRouter(prefix="/faculty", tags=["Faculty"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=list[FacultyResponse])
def get_faculties(db: Session = Depends(get_db)):
    return get_all_faculties(db)

@router.get("/search", response_model=list[FacultyResponse])
def search_faculties(
    name: str,
    db: Session = Depends(get_db)
):
    return search_faculty(db, name)
@router.get("/code/{faculty_code}")
def get_faculty_by_code(
    faculty_code: str,
    db: Session = Depends(get_db)
):
    faculty = get_faculty_details(faculty_code, db)

    if faculty.get("message") == "Faculty not found":
        raise HTTPException(status_code=404, detail="Faculty not found")

    return faculty
@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = get_faculty_by_id(db, faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty
@router.get("/{faculty_id}/location")
def faculty_location(
    faculty_id: int,
    db: Session = Depends(get_db)
):
    location = get_faculty_location(db, faculty_id)

    if not location:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return location


    