from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login",scheme_name="StudentAuth")


def get_current_user(token: str = Depends(oauth2_scheme)):
    rollno = verify_token(token)

    if rollno is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return rollno