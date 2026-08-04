from fastapi import APIRouter,HTTPException
from app.schemas.login import Login
import app.services.auth as auth
from app.token import create_access_token

router = APIRouter(tags=['authentication'])

@router.post("/login")
async def login(request:Login):
    valid = await auth.verify_student(
        request.rollno,
        request.password
    )

    if not valid:
        raise HTTPException(
            status_code=401,
            detail="invalid rollno or password"
        )

    access_token = create_access_token(
        data={"sub": request.rollno}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

