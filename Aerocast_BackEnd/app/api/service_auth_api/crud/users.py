from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.service_auth_api.models.users import User
from app.api.service_auth_api.schemas.users import UserUpdate, UserCreate, UserPublic
from app.core.security import verify_password, get_password_hash


def create_user(*, db: Session, user_data: UserCreate) -> UserPublic:
    """Créer un nouvel utilisateur."""
    hashed_password = get_password_hash(user_data.password)

    db_user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=user_data.is_active,
        is_superuser=user_data.is_superuser,
        role=user_data.role,
        id_compagnie=user_data.id_compagnie,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserPublic.model_validate(db_user)


def update_user(*, db: Session, id: UUID, data: UserUpdate) -> UserPublic | None:
    """Modifier un utilisateur existant."""
    user = db.get(User, id)
    if user is None:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # Si on met à jour le mot de passe → le hasher
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return UserPublic.model_validate(user)


def get_user_by_username(*, db: Session, username: str) -> UserPublic | None:
    """Récupérer un utilisateur par son username."""
    statement = select(User).where(User.username == username)
    user = db.execute(statement).scalar_one_or_none()
    if user is None:
        return None
    return UserPublic.model_validate(user)


def get_user_by_id(*, db: Session, user_id: UUID) -> UserPublic | None:
    """Récupérer un utilisateur par ID."""
    user = db.get(User, user_id)
    if user is None:
        return None
    return UserPublic.model_validate(user)


def authenticate_user(*, db: Session, username: str, password: str) -> UserPublic | None:
    """Authentifier un utilisateur (login)."""
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return UserPublic.model_validate(user)
