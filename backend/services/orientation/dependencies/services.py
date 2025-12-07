from functools import lru_cache
from typing import Generator
from core.config import get_settings, Settings
from core.decision_engine import DecisionEngine
from services.meteo_client import MeteoServiceClient
from services.bagage_client import BagageServiceClient
from services.vol_client import VolServiceClient

@lru_cache()
def get_decision_engine() -> DecisionEngine:
    """Retourne une instance du moteur de décision"""
    settings = get_settings()
    return DecisionEngine(settings)

def get_meteo_client() -> Generator[MeteoServiceClient, None, None]:
    """Retourne un client météo"""
    settings = get_settings()
    client = MeteoServiceClient(settings.METEO_SERVICE_URL)
    try:
        yield client
    finally:
        # Cleanup sera géré par FastAPI
        pass

def get_bagage_client() -> Generator[BagageServiceClient, None, None]:
    """Retourne un client bagages"""
    settings = get_settings()
    client = BagageServiceClient(settings.BAGAGE_SERVICE_URL)
    try:
        yield client
    finally:
        pass

def get_vol_client() -> Generator[VolServiceClient, None, None]:
    """Retourne un client vols"""
    settings = get_settings()
    client = VolServiceClient(settings.VOL_SERVICE_URL)
    try:
        yield client
    finally:
        pass
