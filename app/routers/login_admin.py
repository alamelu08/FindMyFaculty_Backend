from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
from app.core.config import ADMIN_USERNAME,ADMIN_PASSWORD
from app.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(prefix='/login',tags=["Authentication"])


@router.post("/admin")
async def admin_login(request:OAuth2PasswordRequestForm = Depends()):
    print("USERNAME:", repr(request.username))
    print("EXPECTED USERNAME:", repr(ADMIN_USERNAME))

    if(request.username!=ADMIN_USERNAME 
       or request.password!=ADMIN_PASSWORD):
        raise HTTPException(status_code=401, detail="invalid admin credentials")
    
    access_token = create_access_token(
        data={
            "sub": request.username,
            "role": "admin"
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    