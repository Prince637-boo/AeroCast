from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from libs.common.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth.models.user import User
from services.auth.core.roles import UserRole
from libs.common.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise credentials_exception
        
        try:
            user_id = UUID(user_id_str)
        except (ValueError, AttributeError):
            # Si la conversion échoue, le token est invalide
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if not user:
        raise credentials_exception

    return user


def require_role(required: UserRole):
    async def dependency(current_user=Depends(get_current_user)):
        if current_user.role != required:
            raise HTTPException(
                status_code=403,
                detail=f"Role {required} required"
            )
        return current_user
    return dependency
