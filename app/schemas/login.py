from pydantic import BaseModel

class Login(BaseModel):
    rollno:str
    password:str