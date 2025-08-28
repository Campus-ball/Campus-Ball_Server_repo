from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.settings import get_settings
from jose import jwt


bearer_scheme = HTTPBearer(auto_error=True)


def get_current_user_id(cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    settings = get_settings()
    token = cred.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_alg])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return str(user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


