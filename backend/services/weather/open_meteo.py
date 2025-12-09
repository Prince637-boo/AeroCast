import httpx
import logging
from pydantic import ValidationError
from services.weather.config import settings
from services.weather.schemas.open_meteo import OpenMeteoResponse


class OpenMeteoService:
    def __init__(self):
        self.api_url = settings.WEATHER_API_URL
        self.logger = logging.getLogger(__name__)
    
    async def fetch_weather_from_api(self, latitude: float, longitude: float) -> OpenMeteoResponse | None:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.api_url, params=params)
                response.raise_for_status()
                # Valider la réponse avec Pydantic
                return OpenMeteoResponse.model_validate(response.json())
            except httpx.HTTPStatusError as e:
                self.logger.error(f"HTTP error fetching weather data: {e}")
                return None
            except ValidationError as e:
                self.logger.error(f"Invalid data structure from Open-Meteo API: {e}")
                return None