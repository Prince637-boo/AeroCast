from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models.bag import Baggage
from .models.baggage_event import BaggageEvent
from .core.enums import BaggageStatus
import uuid

from .models.scan_log import ScanLog
from .core.utils import generate_qr_code


async def create_baggage(db: AsyncSession, payload):
    tag = f"BG-{uuid.uuid4().hex[:10].upper()}"
    qr = generate_qr_code(tag)

    baggage = Baggage(
        tag=tag,
        owner_id=payload.owner_id,
        company_id=payload.company_id,
        description=payload.description,
        weight=payload.weight,
        status=BaggageStatus.CHECKED_IN,
        qr_code_path=qr
    )
    db.add(baggage)
    await db.commit()
    await db.refresh(baggage)
    return baggage


async def log_scan(db: AsyncSession, baggage_id: str, user_id: str, location: str, device_info: str | None):
    scan = ScanLog(
        baggage_id=baggage_id,
        scanned_by=user_id,
        location=location,
        device_info=device_info
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    return scan


async def update_baggage_status(db: AsyncSession, baggage: Baggage, status: BaggageStatus, location: str):
    baggage.status = status
    event = BaggageEvent(
        baggage_id=baggage.id,
        status=status,
        location=location
    )
    db.add(event)
    await db.commit()
    await db.refresh(baggage)
    return baggage

async def get_baggage(db: AsyncSession, tag: str) -> Baggage | None:
    q = await db.execute(select(Baggage).where(Baggage.tag == tag))
    return q.scalars().first()

async def list_baggages_for_user(db: AsyncSession, user_id: str):
    q = await db.execute(select(Baggage).where(Baggage.owner_id == user_id))
    return q.scalars().all()
