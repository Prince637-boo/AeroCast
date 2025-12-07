import httpx
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MeteoServiceClient:
    """Client pour communiquer avec le service Météo IA"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_meteo_summary(self) -> Dict[str, Any]:
        """Récupère le résumé météo"""
        try:
            response = await self.client.get(f"{self.base_url}/api/meteo/summary")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erreur récupération météo: {e}")
            # Retour par défaut en cas d'erreur
            return {
                "niveau_alerte": "faible",
                "impact": {
                    "capacite_horaire_reduite": 0.0,
                    "retard_moyen": 0,
                    "pistes_principales_disponibles": 3,
                    "secteurs_congestionnes": [],
                    "conditions": []
                }
            }
    
    async def get_forecast(self, hours: int = 3) -> Dict[str, Any]:
        """Récupère les prévisions météo"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/meteo/forecast",
                params={"hours": hours}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erreur récupération prévisions: {e}")
            return {"previsions": []}
    
    async def close(self):
        await self.client.aclose()
