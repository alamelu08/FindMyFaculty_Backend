from typing import Optional
from pydantic import BaseModel

class FacultyCreate(BaseModel):
    name: str
    image_url: str
    cabin: str
    cabin_directions: str
class FacultyResponse(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None
    cabin: str
    cabin_directions: Optional[str] = None
    class Config:
        from_attributes = True
class FacultyUpdate(BaseModel):
    name: str
    image_url: str
    cabin: str
    cabin_directions: str        
