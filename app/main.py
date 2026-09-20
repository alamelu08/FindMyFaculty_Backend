from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base, engine
from app.models import faculty, period, faculty_timetable
from app.routers import admin,faculty,login,login_admin


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin.router)
app.include_router(faculty.router)
app.include_router(login.router)
app.include_router(login_admin.router)

@app.get("/")
def root():
    return {"message": "FindMyFaculty Backend is running!"}

# from fastapi import FastAPI
# from app.database.database import Base, engine
# from app.models import faculty, period, faculty_timetable
# from app.routers import admin,faculty



# app = FastAPI()

# app.include_router(admin.router)
# app.include_router(faculty.router)

# Base.metadata.create_all(bind=engine)

# @app.get("/")
# def root():
#     return {"message": "Hello"}