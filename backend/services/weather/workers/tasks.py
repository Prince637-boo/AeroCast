from libs.common.celery import celery_app
from services.weather.config import settings
from services.weather.services.open_meteo import OpenMeteoService
from services.weather.crud.weather import create_weather_data
from services.weather.schemas.weather import WeatherCreate
from libs.common.database import SessionLocal
import asyncio

async def save_weather_for_location(location):
    service = OpenMeteoService()
    weather_data = await service.fetch_weather_from_api(location["latitude"], location["longitude"])
    
    if weather_data:
        current = weather_data.current_weather
        weather_to_save = WeatherCreate(
            location_name=location["name"],
            latitude=location["latitude"],
            longitude=location["longitude"],
            temperature=current.temperature,
            wind_speed=current.windspeed,
        )
        async with SessionLocal() as db:
            await create_weather_data(db, weather=weather_to_save)
        print(f"Successfully saved weather for {location['name']}")

@celery_app.task(name='services.weather.workers.tasks.fetch_and_save_weather')
def fetch_and_save_weather():
    """
    Tâche Celery pour récupérer et sauvegarder les données météo pour des lieux d'intérêt.
    """
    loop = asyncio.get_event_loop()
    for location in settings.INTEREST_LOCATIONS:
        loop.run_until_complete(save_weather_for_location(location))