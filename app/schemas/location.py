from pydantic import BaseModel
class FacultyLocation(BaseModel):
    faculty_name: str
    location: str
    location_type: str