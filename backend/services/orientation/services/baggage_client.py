from asyncio.log import logger
from datetime import datetime
from typing import Any, Dict
import httpx


class BagageServiceClient:
    """Client pour communiquer avec le service de traçabilité bagages"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_bagage_status(self, id_bagage: str) -> Dict[str, Any]:
        """Récupère le statut d'un bagage"""
        try:
            response = await self.client.get(f"{self.base_url}/api/bag/{id_bagage}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erreur récupération bagage {id_bagage}: {e}")
            # Statut par défaut
            return {
                "id": id_bagage,
                "statut": "ENREGISTRE",
                "position": "Inconnu",
                "horodatage": datetime.now().isoformat()
            }
    
    async def close(self):
        await self.client.aclose()