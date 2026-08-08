from typing import Optional
from pydantic import BaseModel


class FacultyCreate(BaseModel):
    name: str
    cabin: str
    cabin_directions: str


class FacultyUpdate(BaseModel):
    name: str
    cabin: str
    cabin_directions: str


class FacultyResponse(BaseModel):
    id: str
    name: str
    image_url: Optional[str] = None
    cabin: str
    cabin_directions: Optional[str] = None

    class Config:
        from_attributes = True