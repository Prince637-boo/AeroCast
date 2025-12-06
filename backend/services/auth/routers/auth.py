from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import logging
import time
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

from libs.common.database import get_db
from ..models.user import User
from ..models.refresh_token import RefreshToken
from ..schemas.user import UserCreate, UserOut
from ..schemas.company import CompanyCreate, CompanyOut
from ..core.hashing import hash_password, verify_password
from ..core.jwt import create_access_token, generate_refresh_token, hash_refresh_token
from ..core.roles import UserRole
from ..dependencies.user import get_current_user
from ..dependencies.permissions import allow
from ..service_user import create_user, get_user_by_email, get_user_by_id, create_company_and_user, disable_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

tracer = trace.get_tracer(__name__)
logger = logging.getLogger("auth-service")


# -------------------------------
# Helper pour tracer et logger les routes
# -------------------------------
async def traced_route(span_name: str, func, *args, **kwargs):
    start_time = time.time()
    with tracer.start_as_current_span(span_name) as span:
        try:
            result = await func(*args, **kwargs)
            span.set_status(Status(StatusCode.OK))
            return result
        except HTTPException as e:
            span.set_status(Status(StatusCode.ERROR, str(e.detail)))
            logger.error(f"[{span_name}] HTTPException: {e.detail}")
            raise
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            logger.exception(f"[{span_name}] Exception: {str(e)}")
            raise
        finally:
            duration = time.time() - start_time
            logger.info(f"[{span_name}] duration: {duration:.3f}s")


# -------------------------------
# ROUTES
# -------------------------------

@router.post("/register", response_model=UserOut)
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    async def _register():
        q = await db.execute(User.__table__.select().where(User.email == payload.email))
        existing = q.fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered.")

        new_user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            role=payload.role
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    return await traced_route("auth_register", _register)


@router.post("/login")
async def login(payload, request: Request, db: AsyncSession = Depends(get_db)):
    async def _login():
        q = await db.execute(User.__table__.select().where(User.email == payload.email))
        user: User = q.scalar()

        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(str(user.id), user.role.value)
        raw_refresh = generate_refresh_token()
        hashed_refresh = hash_refresh_token(raw_refresh)

        db.add(RefreshToken(
            user_id=user.id,
            token=hashed_refresh,
            user_agent=request.headers.get("user-agent", "unknown"),
            ip_address=request.client.host,
            expires_at=RefreshToken.expiry(days=7),
        ))
        await db.commit()

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh,
            "token_type": "bearer"
        }

    return await traced_route("auth_login", _login)


@router.post("/refresh")
async def refresh(refresh_token: str, request: Request, db: AsyncSession = Depends(get_db)):
    async def _refresh():
        hashed = hash_refresh_token(refresh_token)
        q = await db.execute(RefreshToken.__table__.select().where(RefreshToken.token == hashed))
        token_record = q.scalar()

        if not token_record or token_record.is_revoked:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        if token_record.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")

        token_record.is_revoked = True

        new_raw = generate_refresh_token()
        new_hash = hash_refresh_token(new_raw)

        db.add(RefreshToken(
            user_id=token_record.user_id,
            token=new_hash,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host,
            expires_at=RefreshToken.expiry(days=7),
        ))
        await db.commit()

        access = create_access_token(str(token_record.user_id), "PASSAGER")
        return {"access_token": access, "refresh_token": new_raw}

    return await traced_route("auth_refresh", _refresh)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    async def _me():
        return current_user

    return await traced_route("auth_me", _me)


# -------------------------------
# ADMIN ROUTES
# -------------------------------

@router.post("/admin/create/company", response_model=CompanyOut)
async def admin_create_company(company: CompanyCreate, user_payload: UserCreate,
                               db: AsyncSession = Depends(get_db),
                               admin = Depends(allow(UserRole.ADMIN))):
    async def _create_company():
        company_obj, user_obj = await create_company_and_user(db, company, user_payload)
        return company_obj

    return await traced_route("admin_create_company", _create_company)


@router.post("/admin/create/atc", response_model=UserOut)
async def admin_create_atc(payload: UserCreate, db: AsyncSession = Depends(get_db), admin = Depends(allow(UserRole.ADMIN))):
    async def _create_atc():
        payload.role = UserRole.ATC
        if await get_user_by_email(db, payload.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        user = await create_user(db, payload)
        return user

    return await traced_route("admin_create_atc", _create_atc)


@router.get("/admin/users", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), admin = Depends(allow(UserRole.ADMIN))):
    async def _list_users():
        q = await db.execute(select(User))
        return q.scalars().all()

    return await traced_route("admin_list_users", _list_users)


@router.patch("/admin/users/{user_id}/disable", response_model=UserOut)
async def admin_disable_user(user_id: str, db: AsyncSession = Depends(get_db), admin = Depends(allow(UserRole.ADMIN))):
    async def _disable_user():
        user = await get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return await disable_user(db, user)

    return await traced_route(f"admin_disable_user:{user_id}", _disable_user)
