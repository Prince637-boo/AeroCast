from backend.services.orientation.utils import generer_alertes, generer_instructions, log_orientation
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import Optional
from datetime import datetime
import logging

from schemas.orientation import (
    OrientationRequest,
    OrientationResponse,
    InstructionSchema,
    AlerteSchema,
    EtapeParcoursSchema,
    SituationSchema,
    TypeInstruction,
    ActionType
)
from core.decision_engine import DecisionEngine
from services.meteo_client import MeteoServiceClient
from services.bagage_client import BagageServiceClient
from services.vol_client import VolServiceClient
from dependencies.services import (
    get_decision_engine,
    get_meteo_client,
    get_bagage_client,
    get_vol_client
)
from dependencies.validation import OrientationValidator

router = APIRouter(
    prefix="/api/orientation",
    tags=["Orientation Passagers"]
)

logger = logging.getLogger(__name__)


@router.get(
    "/{numero_vol}/{id_bagage}",
    response_model=OrientationResponse,
    summary="Obtenir l'orientation pour un passager",
    description="Calcule l'orientation optimale basée sur la météo, le bagage et le vol"
)
async def get_orientation(
    numero_vol: str,
    id_bagage: str,
    position_estimee: Optional[str] = None,
    decision_engine: DecisionEngine = Depends(get_decision_engine),
    meteo_client: MeteoServiceClient = Depends(get_meteo_client),
    bagage_client: BagageServiceClient = Depends(get_bagage_client),
    vol_client: VolServiceClient = Depends(get_vol_client),
    background_tasks: BackgroundTasks = None
):
    """
    Endpoint principal pour obtenir l'orientation d'un passager.
    
    Args:
        numero_vol: Numéro du vol (ex: AF1234)
        id_bagage: Identifiant du bagage
        position_estimee: Position actuelle du passager (optionnel)
    
    Returns:
        OrientationResponse avec instructions détaillées
    """
    try:
        # Validation
        numero_vol = OrientationValidator.validate_numero_vol(numero_vol)
        id_bagage = OrientationValidator.validate_id_bagage(id_bagage)
        position_estimee = OrientationValidator.validate_position(position_estimee)
        
        logger.info(f"Calcul orientation pour vol {numero_vol}, bagage {id_bagage}")
        
        # 1. Récupération des données en parallèle
        meteo_data = await meteo_client.get_meteo_summary()
        bagage_data = await bagage_client.get_bagage_status(id_bagage)
        vol_data = await vol_client.get_vol_info(numero_vol)
        
        # 2. Analyse de la situation
        situation = decision_engine.analyser_situation(
            meteo_data, bagage_data, vol_data
        )
        
        # 3. Génération des instructions
        instructions = generer_instructions(
            decision_engine,
            situation,
            position_estimee,
            vol_data,
            bagage_data
        )
        
        # 4. Génération des alertes
        alertes = generer_alertes(situation, meteo_data, vol_data)
        
        # 5. Génération du parcours
        parcours = decision_engine.generer_parcours_jitb(
            situation, vol_data, position_estimee
        )
        
        # 6. Log en arrière-plan (optionnel)
        if background_tasks:
            background_tasks.add_task(
                log_orientation,
                numero_vol, id_bagage, situation, instructions
            )
        
        return OrientationResponse(
            success=True,
            numero_vol=numero_vol,
            timestamp=datetime.utcnow(),
            situation=SituationSchema(**situation),
            instructions=[InstructionSchema(**inst) for inst in instructions],
            alertes=[AlerteSchema(**alert) for alert in alertes],
            parcours=[EtapeParcoursSchema(**etape) for etape in parcours]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du calcul de l'orientation"
        )


@router.post(
    "/",
    response_model=OrientationResponse,
    summary="Obtenir l'orientation (POST)",
    description="Alternative POST pour obtenir l'orientation"
)
async def post_orientation(
    request: OrientationRequest,
    decision_engine: DecisionEngine = Depends(get_decision_engine),
    meteo_client: MeteoServiceClient = Depends(get_meteo_client),
    bagage_client: BagageServiceClient = Depends(get_bagage_client),
    vol_client: VolServiceClient = Depends(get_vol_client)
):
    """Endpoint POST pour obtenir l'orientation"""
    return await get_orientation(
        numero_vol=request.numero_vol,
        id_bagage=request.id_bagage,
        position_estimee=request.position_estimee,
        decision_engine=decision_engine,
        meteo_client=meteo_client,
        bagage_client=bagage_client,
        vol_client=vol_client
    )


@router.get(
    "/health",
    summary="Vérification de santé du service",
    tags=["Health"]
)
async def health_check():
    """Endpoint de santé"""
    return {
        "status": "healthy",
        "service": "orientation-service",
        "timestamp": datetime.utcnow().isoformat()
    }
