from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.schemas.faculty import FacultyCreate, FacultyUpdate, FacultyResponse
from app.services.faculty_services import (
    create_faculty,
    update_faculty,
    delete_faculty,
)

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/faculty", response_model=FacultyResponse)
def add_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    return create_faculty(db, faculty)

@router.put("/faculty/{faculty_id}", response_model=FacultyResponse)
def edit_faculty(
    faculty_id: int,
    faculty: FacultyUpdate,
    db: Session = Depends(get_db)
):
    updated_faculty = update_faculty(db, faculty_id, faculty)
    if not updated_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return updated_faculty

@router.delete("/faculty/{faculty_id}")
def remove_faculty(
    faculty_id: int,
    db: Session = Depends(get_db)
):
    deleted_faculty = delete_faculty(db, faculty_id)
    if not deleted_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return {"message": "Faculty deleted successfully"}