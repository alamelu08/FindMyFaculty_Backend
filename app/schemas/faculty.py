from pydantic import BaseModel
class FacultyCreate(BaseModel):
    name: str
    image_url: str
    cabin: str
    cabin_directions: str
class FacultyResponse(BaseModel):
    id: int
    name: str
    image_url: str
    cabin: str
    cabin_directions: str
    class Config:
        from_attributes = True
class FacultyUpdate(BaseModel):
    name: str
    image_url: str
    cabin: str
    cabin_directions: str        