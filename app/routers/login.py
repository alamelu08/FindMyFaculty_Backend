from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
import app.services.auth as auth
from app.token import create_access_token

router = APIRouter()

@router.post("/login",tags=["Authentication"])
async def login(request: OAuth2PasswordRequestForm = Depends()):

    clean_roll = (request.username or "").strip().upper()

    valid = await auth.verify_student(
        clean_roll,
        request.password
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="invalid rollno or password"
        )

    access_token = create_access_token(
        data={"sub": clean_roll}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

