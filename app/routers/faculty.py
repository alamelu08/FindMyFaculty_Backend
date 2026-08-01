from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.faculty import FacultyResponse
from app.services.faculty_services import (
    get_all_faculties,
    get_faculty_by_id, search_faculty
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

@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = get_faculty_by_id(db, faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty


    