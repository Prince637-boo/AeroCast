from http.client import HTTPException
from typing import Any, Dict
from fastapi import logger
import httpx


class VolServiceClient:
    """Client pour communiquer avec le service de gestion des vols"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def get_vol_info(self, numero_vol: str) -> Dict[str, Any]:
        """Récupère les informations d'un vol"""
        try:
            response = await self.client.get(f"{self.base_url}/api/vol/{numero_vol}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Erreur récupération vol {numero_vol}: {e}")
            raise HTTPException(
                status_code=404,
                detail=f"Vol {numero_vol} non trouvé"
            )
    
    async def close(self):
        await self.client.aclose()
