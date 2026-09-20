from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
import app.services.auth as auth
from app.token import create_access_token

router = APIRouter()

@router.post("/login",tags=["Authentication"])
async def login(request: OAuth2PasswordRequestForm = Depends()):

    rollno = request.username.strip().upper()

    if len(rollno) < 3 or rollno[2] not in {"Z", "N"}:
        raise HTTPException(
            status_code=403,
            detail="Sorry, access is currently limited to CSE department students."
        )
    
    valid = await auth.verify_student(
        rollno,
        request.password
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="invalid rollno or password"
        )

    access_token = create_access_token(
        data={"sub": rollno}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

