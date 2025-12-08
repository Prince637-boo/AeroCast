import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from services.auth.main import app
from libs.common.database import get_db
from tests.utils.db import init_test_db, drop_test_db, AsyncTestingSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth.models.user import User, UserRole
from libs.common.security import hash_password
from services.auth.core.jwt import create_access_token
from services.auth.models.company import Company


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_database():
    await init_test_db()
    yield
    await drop_test_db()


@pytest_asyncio.fixture
async def db_session():
    async with AsyncTestingSessionLocal() as session:
        yield session
        await session.rollback()



@pytest_asyncio.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()

import uuid

@pytest_asyncio.fixture
async def admin_user(db_session):
    admin = User(
        email=f"admin_{uuid.uuid4()}@test.com",
        hashed_password=hash_password("adminpass"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin



@pytest_asyncio.fixture
async def admin_token(client, admin_user):
    # Login admin et récupère access_token
    resp = await client.post("/auth/login", data={
        "username": admin_user.email,
        "password": "adminpass"
    })
    data = resp.json()
    assert "access_token" in data, "Login failed: no access_token returned"
    return data["access_token"]


@pytest_asyncio.fixture
async def create_users(db_session: AsyncSession):
    """
    Crée admin, company, ATC et passenger avec tokens uniques.
    """
    # Nom de compagnie unique
    company_name = f"TestAir-{uuid.uuid4().hex[:6]}"
    company = Company(name=company_name)
    db_session.add(company)
    await db_session.flush()

    # Utilisateurs
    admin = User(
        email=f"admin_{uuid.uuid4().hex[:6]}@test.com",
        hashed_password=hash_password("adminpass"),
        role=UserRole.ADMIN,
        is_active=True
    )
    company_user = User(
        email=f"company_{uuid.uuid4().hex[:6]}@test.com",
        hashed_password=hash_password("companypass"),
        role=UserRole.COMPAGNIE,
        company=company,
        is_active=True
    )
    atc = User(
        email=f"atc_{uuid.uuid4().hex[:6]}@test.com",
        hashed_password=hash_password("atcpass"),
        role=UserRole.ATC,
        is_active=True
    )
    pax = User(
        email=f"pax_{uuid.uuid4().hex[:6]}@test.com",
        hashed_password=hash_password("paxpass"),
        role=UserRole.PASSAGER,
        is_active=True
    )

    db_session.add_all([admin, company_user, atc, pax])
    await db_session.commit()

    # Tokens
    tokens = {
        "admin": create_access_token(data={"sub": str(admin.id), "role": admin.role.value}),
        "company": create_access_token(data={"sub": str(company_user.id), "role": company_user.role.value}),
        "atc": create_access_token(data={"sub": str(atc.id), "role": atc.role.value}),
        "pax": create_access_token(data={"sub": str(pax.id), "role": pax.role.value}),
    }

    return {"users": {"admin": admin, "company": company_user, "atc": atc, "pax": pax},
            "company": company,
            "tokens": tokens}
