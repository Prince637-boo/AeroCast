from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from libs.common.database import get_db
from services.weather.schemas.weather import Weather as WeatherSchema, WeatherCreate
from services.weather.crud.weather import get_latest_weather_by_coords, create_weather_data
from services.weather.services.open_meteo import OpenMeteoService

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/", response_model=WeatherSchema)
async def get_weather(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    db: AsyncSession = Depends(get_db),
    open_meteo_service: OpenMeteoService = Depends()
):
    # 1. Vérifier si des données récentes existent en BDD
    db_weather = await get_latest_weather_by_coords(db, lat=latitude, lon=longitude)
    if db_weather:
        return db_weather

    # 2. Sinon, appeler l'API externe
    weather_data = await open_meteo_service.fetch_weather_from_api(latitude, longitude)
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found for the given coordinates.")

    current = weather_data.current_weather
    
    # 3. Sauvegarder les nouvelles données en BDD
    weather_to_save = WeatherCreate(
        location_name="N/A", # Le nom pourrait être résolu via un autre service
        latitude=weather_data.latitude,
        longitude=weather_data.longitude,
        temperature=current.temperature,
        wind_speed=current.windspeed,
    )
    new_db_weather = await create_weather_data(db, weather=weather_to_save)
    
    return new_db_weather