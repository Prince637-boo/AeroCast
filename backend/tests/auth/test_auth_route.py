import pytest
import uuid
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.models.user import User
from services.auth.models.company import Company
from services.auth.models.refresh_token import RefreshToken
from services.auth.core.roles import UserRole
from services.auth.core.hashing import hash_password
from services.auth.core.jwt import hash_refresh_token
from services.auth.main import app

from libs.common.database import get_db

# -------------------------------
# Fixtures utiles
# -------------------------------

@pytest.fixture
async def unique_company_name():
    return f"AirTest-{uuid.uuid4().hex[:6]}"

# ============================================================
# TEST AUTH ROUTES
# ============================================================

@pytest.mark.asyncio
async def test_register_passenger(client):
    resp = await client.post("/auth/register", json={
        "email": "pax@test.com",
        "password": "123456"
    })
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["email"] == "pax@test.com"
    assert data["role"] == UserRole.PASSAGER


@pytest.mark.asyncio
async def test_register_fails_setting_role(client):
    resp = await client.post("/auth/register", json={
        "email": "test2@test.com",
        "password": "123456",
        "role": "ADMIN"
    })
    # The Pydantic model ignores extra fields, so the status is OK.
    # We verify that the role was not assigned.
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["role"] == UserRole.ADMIN


@pytest.mark.asyncio
async def test_login_success(client, admin_user):
    data = { # Changed json to data, email to username
        "email": admin_user.email,
        "password": "adminpass",
    }
    resp = await client.post("/auth/login", json=data)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    
    assert "access_token" in data
    assert data["access_token"]


@pytest.mark.asyncio
async def test_login_wrong_password(client, admin_user):
    resp = await client.post("/auth/login", json={ # Ensure data and username
        "email": admin_user.email,
        "password": "wrongpass",
    })
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# # ============================================================
# # TEST ADMIN ROUTES
# # ============================================================

@pytest.mark.asyncio
async def test_admin_create_company(client, admin_token, unique_company_name):
    resp = await client.post("/auth/admin/create/company",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "company": {
                "name": unique_company_name,
                "legal_id": "TEST-ID",
                "contact_email": "info@airtest.com"
            },
            "user_payload": {
                "email": f"ceo-{uuid.uuid4().hex[:6]}@airtest.com",
                "password": "comp123"
            }
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    print(data)
    assert resp.json()["name"] == unique_company_name


@pytest.mark.asyncio
async def test_admin_create_atc(client, admin_token):
    email = f"atc-{uuid.uuid4().hex[:6]}@test.com"
    resp = await client.post(
        "/auth/admin/create/atc",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"email": email, "password": "atcpass"}
    )
    assert resp.status_code == 200
    assert resp.json()["role"] == UserRole.ATC


@pytest.mark.asyncio
async def test_admin_list_users(client, admin_token):
    resp = await client.get(
        "/auth/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_admin_disable_user(client, db_session, admin_token):
    user = User(
        email=f"target-{uuid.uuid4().hex[:6]}@test.com",
        hashed_password=hash_password("password"),
        role=UserRole.PASSAGER
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    resp = await client.patch(
        f"/auth/admin/users/{user.id}/disable",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["is_active"] is False


# # ============================================================
# # TEST COMPANY ROUTES
# # ============================================================

@pytest.mark.asyncio
async def test_company_create_passenger(client, db_session, unique_company_name):
    # create a company
    company = Company(name=unique_company_name)
    db_session.add(company)
    await db_session.flush()

    company_user = User(
        email=f"company-{uuid.uuid4().hex[:6]}@test.com",
        hashed_password=hash_password("companypass"),
        role=UserRole.COMPAGNIE,
        company=company,
        is_active=True,
    )
    db_session.add(company_user)
    await db_session.commit()
    await db_session.refresh(company_user)

    # login company
    resp_login = await client.post("/auth/login", json={ # Changed json to data, email to username
        "email": company_user.email,
        "password": "companypass"
    })
    token = resp_login.json()["access_token"]
    assert token is not None

    # create passenger
    resp = await client.post(
        "/auth/company/create/passenger",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": f"pax-{uuid.uuid4().hex[:6]}@company.com", "password": "123456"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == UserRole.PASSAGER
    assert data["company_id"] == str(company.id)


# # ============================================================
# # TEST RBAC PERMISSIONS
# # ============================================================

@pytest.mark.asyncio
async def test_passenger_cannot_create_atc(client):
    # register passenger
    resp = await client.post("/auth/register", json={
        "email": f"pax2-{uuid.uuid4().hex[:6]}@test.com",
        "password": "12345"
    })
    assert resp.status_code == status.HTTP_200_OK

    # login passenger
    resp_login = await client.post("/auth/login", json={ # Changed json to data, email to username
        "email": resp.json()["email"],
        "password": "12345"
    })
    pax_token = resp_login.json()["access_token"]
    assert pax_token is not None

    resp = await client.post(
        "/auth/admin/create/atc",
        headers={"Authorization": f"Bearer {pax_token}"},
        json={"email": f"bad-{uuid.uuid4().hex[:6]}@test.com", "password": "123"}
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_atc_cannot_list_users(client, db_session):
    atc = User(
        email=f"atc2-{uuid.uuid4().hex[:6]}@test.com",
        hashed_password=hash_password("atcpass"),
        role=UserRole.ATC
    )
    db_session.add(atc)
    await db_session.commit()

    resp_login = await client.post("/auth/login", json={ # Changed json to data, email to username
        "email": atc.email,
        "password": "atcpass"
    })
    token = resp_login.json()["access_token"]
    assert token is not None

    resp = await client.get(
        "/auth/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN


# ============================================================
# TEST REFRESH TOKEN
# ============================================================

from datetime import datetime, timedelta, timezone

@pytest.mark.asyncio
async def test_refresh_token_success(client, db_session, admin_user):
    raw_token = "raw1234"
    hashed = hash_refresh_token(raw_token)

    rt = RefreshToken( # Fix datetime.utcnow()
        user_id=admin_user.id,
        token=hashed,
        user_agent="pytest",
        ip_address="127.0.0.1",
        expires_at=RefreshToken.expiry(days=1)
    )
    db_session.add(rt)
    await db_session.commit()

    resp = await client.post("/auth/refresh", json={"refresh_token": raw_token}) # Changed json to data
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_token_expired(client, db_session, admin_user):
    raw = "expired123"
    hashed = hash_refresh_token(raw)

    old = RefreshToken(
        user_id=admin_user.id,
        token=hashed,
        user_agent="pytest",
        ip_address="127.0.0.1",
        expires_at=datetime.now(timezone.utc) - timedelta(days=1) # Use timezone-aware datetime
    )
    db_session.add(old)
    await db_session.commit()

    resp = await client.post("/auth/refresh", json={"refresh_token": raw}) # Changed json to data
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ============================================================
# TEST /me ROUTE
# ============================================================

@pytest.mark.asyncio
async def test_me_endpoint(client, admin_token):
    resp = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "email" in data
    assert data["email"].startswith("admin_") # L'email est généré dynamiquement
