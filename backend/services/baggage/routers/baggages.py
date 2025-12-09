from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
import logging
import time

from libs.common.database import get_db
from services.auth.dependencies.user import get_current_user
from services.auth.dependencies.permissions import allow
from services.auth.core.roles import UserRole

from ..schemas.bag import BaggageCreate, BaggageOut
from ..schemas.baggage_event import BaggageEventCreate
from ..schemas.scan_log import ScanLogCreate, ScanLogOut
from ..baggage_service import (
    create_baggage,
    update_baggage_status,
    get_baggage,
    list_baggages_for_user,
    log_scan,
)

router = APIRouter(prefix="/baggages", tags=["Baggages"])
tracer = trace.get_tracer(__name__)
logger = logging.getLogger("baggage-service")


# -------------------------------
# Dependable pour vérifier l'existence du bagage
# -------------------------------
async def get_existing_baggage(tag: str, db: AsyncSession = Depends(get_db)):
    """
    Vérifie si un bagage existe à partir de son tag.
    Retourne le bagage si trouvé, sinon lève une HTTPException 404.
    """
    baggage = await get_baggage(db, tag)
    if not baggage:
        raise HTTPException(status_code=404, detail="Baggage not found")
    return baggage


# -------------------------------
# Helper pour tracer et logger les routes
# -------------------------------
async def traced_route(span_name: str, func, *args, **kwargs):
    """
    Wrapper pour tracer l'exécution d'une route avec OpenTelemetry
    et logger la durée et les exceptions.
    """
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
# Routes
# -------------------------------

@router.post(
    "/",
    response_model=BaggageOut,
    summary="Créer un nouveau bagage",
    response_description="Détails du bagage créé"
)
async def add_baggage(
    payload: BaggageCreate,
    db: AsyncSession = Depends(get_db),
    company=Depends(allow(UserRole.COMPAGNIE, UserRole.ADMIN)),
):
    """
    Permet à une compagnie ou un admin de créer un nouveau bagage.
    """
    return await traced_route("add_baggage", create_baggage, db, payload)


@router.post(
    "/{tag}/status",
    response_model=BaggageOut,
    summary="Mettre à jour le statut d'un bagage",
    response_description="Bagage mis à jour"
)
async def change_status(
    tag: str,
    event: BaggageEventCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(allow(UserRole.COMPAGNIE, UserRole.ADMIN, UserRole.ATC)),
    baggage=Depends(get_existing_baggage),
):
    """
    Permet de mettre à jour le statut d'un bagage avec son emplacement.
    Accessible par la compagnie, l'ATC ou l'admin.
    """
    async def _update():
        return await update_baggage_status(db, baggage, event.status, event.location)

    return await traced_route(f"change_status:{tag}", _update)


# -------------------------------
# Routes pour les utilisateurs
# -------------------------------

@router.get(
    "/{tag}",
    response_model=BaggageOut,
    summary="Consulter le statut d'un bagage",
    response_description="Détails du bagage"
)
async def get_baggage_info(
    tag: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
    baggage=Depends(get_existing_baggage),
):
    """
    Permet à un passager de consulter le statut de son bagage spécifique.
    Les compagnies et admins peuvent consulter n'importe quel bagage.
    """
    async def _get():
        if user.role == UserRole.PASSAGER and baggage.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")
        return baggage

    return await traced_route(f"get_baggage_info:{tag}", _get)


@router.get(
    "/my/list",
    response_model=list[BaggageOut],
    summary="Liste des bagages du passager",
    response_description="Liste des bagages appartenant au passager"
)
async def my_baggages(
    db: AsyncSession = Depends(get_db),
    user=Depends(allow(UserRole.PASSAGER)),
):
    """
    Retourne tous les bagages appartenant au passager connecté.
    """
    async def _list():
        return await list_baggages_for_user(db, user.id)

    return await traced_route("my_baggages", _list)


@router.post(
    "/{tag}/scan",
    response_model=ScanLogOut,
    summary="Ajouter un log de scan pour un bagage",
    response_description="Log de scan créé"
)
async def scan_baggage(
    tag: str,
    payload: ScanLogCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(allow(UserRole.COMPAGNIE, UserRole.ATC, UserRole.ADMIN)),
    baggage=Depends(get_existing_baggage),
):
    """
    Permet à une compagnie, un ATC ou un admin de créer un log de scan
    pour un bagage à un endroit précis avec des informations sur l'appareil.
    """
    async def _scan():
        return await log_scan(
            db=db,
            baggage_id=baggage.id,
            user_id=user.id,
            location=payload.location,
            device_info=payload.device_info,
        )

    return await traced_route(f"scan_baggage_route:{tag}", _scan)
