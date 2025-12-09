from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from services.weather.models.weather import Weather
from services.weather.schemas.weather import WeatherCreate
from datetime import datetime, timedelta

async def get_latest_weather_by_coords(db: AsyncSession, lat: float, lon: float, max_age_hours: int = 1):
    """
    Récupère le relevé météo le plus récent pour des coordonnées données,
    s'il n'est pas plus vieux que max_age_hours.
    """
    stmt = select(Weather).where(
        Weather.latitude == lat,
        Weather.longitude == lon,
        Weather.timestamp >= datetime.utcnow() - timedelta(hours=max_age_hours)
    ).order_by(Weather.timestamp.desc())
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_weather_data(db: AsyncSession, weather: WeatherCreate):
    db_weather = Weather(**weather.model_dump())
    db.add(db_weather)
    await db.commit()
    await db.refresh(db_weather)
    return db_weather