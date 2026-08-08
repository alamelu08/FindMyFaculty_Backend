from fastapi import UploadFile, File
import os
import shutil
from app.services.timetable_service import upload_timetable_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.dependencies.admin_auth import get_current_admin
from app.schemas.faculty import FacultyCreate, FacultyUpdate, FacultyResponse
from app.services.faculty_services import (
    create_faculty,
    update_faculty,
    delete_faculty,
)

router = APIRouter(prefix="/admin", tags=["Admin"],dependencies=[Depends(get_current_admin)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/faculty", response_model=FacultyResponse)
def add_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    return create_faculty(db, faculty)

@router.put("/faculty/{faculty_name}", response_model=FacultyResponse)
def edit_faculty(
    faculty_name: str,
    faculty: FacultyUpdate,
    db: Session = Depends(get_db)
):
    updated_faculty = update_faculty(db, faculty_name, faculty)

    if not updated_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return updated_faculty

@router.delete("/faculty/{faculty_name}")
def remove_faculty(
    faculty_name: str,
    db: Session = Depends(get_db)
):
    deleted_faculty = delete_faculty(db, faculty_name)

    if not deleted_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return {"message": "Faculty deleted successfully"}
@router.post("/upload-timetable")
async def upload_timetable(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return upload_timetable_service(file_path, db)