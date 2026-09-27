from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="StudentAuth", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme)):
    if token:
        rollno = verify_token(token)
        if rollno is not None:
            return rollno

    # Allow student browsing
    return "student_user"