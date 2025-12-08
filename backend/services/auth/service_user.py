from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from services.auth.models.user import User
from services.auth.models.company import Company
from services.auth.core.hashing import hash_password
from services.auth.core.roles import UserRole
from services.auth.schemas.user import UserCreate
from uuid import UUID

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    q = await db.execute(select(User).where(User.email == email))
    return q.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    q = await db.execute(select(User).where(User.id == user_id))
    return q.scalars().first()

async def create_user(db: AsyncSession, payload: UserCreate, creator_role: UserRole = None, company: Company | None = None) -> User:

    role = payload.role or UserRole.PASSAGER

    hashed = hash_password(payload.password)
    new = User(email=payload.email, hashed_password=hashed, role=role, company=company)
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return new

async def create_company_and_user(db: AsyncSession, company_payload, user_payload) -> tuple[Company, User]:

    company = Company(name=company_payload.name, legal_id=company_payload.legal_id, contact_email=company_payload.contact_email)
    db.add(company)
    await db.flush() 
    user_payload.role = UserRole.COMPAGNIE
    user = User(email=user_payload.email, hashed_password=hash_password(user_payload.password), role=UserRole.COMPAGNIE, company_id=company.id)
    db.add(user)
    await db.commit()
    await db.refresh(company)
    await db.refresh(user)  
    return company, user

async def disable_user(db: AsyncSession, user: User):
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return user

async def create_passenger_for_company(
    db: AsyncSession,
    company_id: UUID,
    email: str,
    password: str
) -> User:
    """
    Crée un passager associé à une compagnie.
    
    Args:
        db: Session de base de données
        company_id: UUID de la compagnie
        email: Email du passager
        password: Mot de passe du passager
    
    Returns:
        User créé
    """
    # Vérifier email unique
    existing = await get_user_by_email(db, email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Créer le passager
    passenger = User(
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.PASSAGER,
        company_id=company_id,
        is_active=True
    )
    
    db.add(passenger)
    await db.commit()
    await db.refresh(passenger)
    
    return passenger
