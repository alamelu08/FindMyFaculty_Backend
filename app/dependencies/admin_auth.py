from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.token import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/admin", scheme_name="AdminAuth")


def get_current_admin(
    token: str = Depends(oauth2_scheme)
):
    try:
        from jose import jwt
        from app.token import SECRET_KEY, ALGORITHM

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        role = payload.get("role")

        if role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )

        return payload.get("sub")

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired admin token"
        )