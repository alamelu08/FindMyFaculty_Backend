from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
import app.services.auth as auth
from app.token import create_access_token

router = APIRouter()

@router.post("/login",tags=["Authentication"])
async def login(request: OAuth2PasswordRequestForm = Depends()):

    valid = await auth.verify_student(
        request.username,
        request.password
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="invalid rollno or password"
        )

    access_token = create_access_token(
        data={"sub": request.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

