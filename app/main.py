from fastapi import FastAPI
from app.database.database import Base, engine
from app.models import faculty, period, faculty_timetable
from app.routers import admin,faculty

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(admin.router)
app.include_router(faculty.router)

@app.get("/")
def root():
    return {"message": "FindMyFaculty Backend is running!"}