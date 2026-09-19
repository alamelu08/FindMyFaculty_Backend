from typing import Optional
from pydantic import BaseModel, Field


class FacultyCreate(BaseModel):
    name: str
    cabin: str
    cabin_directions: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "name": "string",
                "cabin": "string",
                "cabin_directions": "string"
            }
        }
    }


class FacultyUpdate(BaseModel):
    cabin: Optional[str] = None
    cabin_directions: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "cabin": "string",
                "cabin_directions": "string"
            }
        }
    }


class FacultyResponse(BaseModel):
    id: str
    name: str
    image_url: Optional[str] = None
    cabin: str
    cabin_directions: Optional[str] = None

    model_config = {
        "from_attributes": True
    }