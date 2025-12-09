import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from services.weather.main import app
from services.weather.crud.weather import create_weather_data
from services.weather.schemas.weather import WeatherCreate
from services.weather.schemas.open_meteo import OpenMeteoResponse
from datetime import datetime

# On utilise le client de test défini dans conftest.py, qui gère la BDD de test
pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_open_meteo_service():
    """Fixture pour mocker le service OpenMeteo."""
    # Données de réponse simulées de l'API Open-Meteo
    mock_response = {
        "latitude": 48.88,
        "longitude": 2.36,
        "current_weather": {
            "temperature": 15.0,
            "windspeed": 10.0,
            "weathercode": 3,
            "time": "2023-10-27T12:00"
        }
    }
    
    # Création du mock
    mock_service = MagicMock()
    mock_service.fetch_weather_from_api.return_value = OpenMeteoResponse.model_validate(mock_response)
    
    return mock_service


async def test_get_weather_from_api_when_db_is_empty(client: AsyncClient, mock_open_meteo_service):
    """
    Test: L'endpoint doit appeler l'API externe si la BDD est vide
    et retourner les données formatées.
    """
    # Remplacement de la dépendance par notre mock
    from services.weather.services.open_meteo import OpenMeteoService
    app.dependency_overrides[OpenMeteoService] = lambda: mock_open_meteo_service

    lat, lon = 48.88, 2.36
    response = await client.get(f"/weather/?latitude={lat}&longitude={lon}")

    assert response.status_code == 200
    data = response.json()
    assert data["latitude"] == lat
    assert data["longitude"] == lon
    assert data["temperature"] == 15.0
    assert data["wind_speed"] == 10.0
    
    # Nettoyage de l'override pour ne pas affecter les autres tests
    app.dependency_overrides.clear()


async def test_get_weather_from_db_when_data_is_recent(client: AsyncClient, db_session: AsyncSession):
    """
    Test: L'endpoint doit retourner les données de la BDD si elles sont récentes,
    sans appeler l'API externe.
    """
    # Pré-remplir la BDD avec des données récentes
    lat, lon = 51.50, -0.12
    weather_in_db = await create_weather_data(db_session, WeatherCreate(
        location_name="London",
        latitude=lat,
        longitude=lon,
        temperature=12.5,
        wind_speed=5.5
    ))

    response = await client.get(f"/weather/?latitude={lat}&longitude={lon}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == weather_in_db.id
    assert data["temperature"] == 12.5
    assert data["location_name"] == "London"