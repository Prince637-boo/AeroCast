from typing import Any
from uuid import UUID

from sqlalchemy import func, select

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from app.models.users import User
from app.core.security import verify_password, get_password_hash
from app.api.service_auth_api.crud import users
from app.api.service_auth_api.schemas.message import Message
from app.api.deps import (SessionDeps, CurrentUser, get_current_active_admin)
from app.api.service_auth_api.schemas.users import (
    UserPublic,
    UsersPublic,
    UserCreate
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", dependencies=[Depends(get_current_active_admin)], response_model=UsersPublic)
def read_users(db: SessionDeps, skip: int = 0, limit: int = 100):
    """
    Récupérer tous les utilisateurs
    """
    count_statement = select(func.count()).select_from(User)
    count = db.execute(count_statement).scalar()

    statement = select(User).offset(skip).limit(limit)
    users = db.execute(statement).scalars().all()
    
    return UsersPublic.model_validate({"data":users, "count":count})
    
@router.post("/create", dependencies=[Depends(get_current_active_admin)], response_model=UserPublic )
def create_user(*, db: SessionDeps, user_in: UserCreate) -> Any:
    """
    Créer un utilisateur 
    """
    user = users.get_user_by_username(db=db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400, 
            detail="Un utilisateur avec ce username existe déjà"
        )
    user = users.create_user(db=db, user_data=user_in)
    return user