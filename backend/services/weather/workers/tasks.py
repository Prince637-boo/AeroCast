from celery import Celery
from .models.prediction import fetch_weather_data, parse_weather_data
from .models.database import SessionLocal, WeatherPrediction
from ..config import settings

# Crée l'application Celery avec le broker URL depuis les settings
app = Celery("tasks", broker=settings.CELERY_BROKER_URL)

# Configure Celery Beat pour exécuter la tâche périodiquement
app.conf.beat_schedule = {
    'update-weather-periodically': {
        'task': 'services.weather.workers.tasks.update_weather_periodically',
        'schedule': 3600.0,  # Exécute toutes les heures (en secondes)
    },
}

@app.task
def update_weather_periodically():
    locations = [(48.8566, 2.3522), (51.5074, -0.1278)]  # Paris, Londres
    db = SessionLocal()
    try:
        for lat, lon in locations:
            raw_data = fetch_weather_data(lat, lon)
            weather_data = parse_weather_data(raw_data)
            prediction = WeatherPrediction(
                latitude=lat,
                longitude=lon,
                temperature=weather_data.temperature,
                humidity=weather_data.humidity,
                wind_speed=weather_data.wind_speed,
                precipitation=weather_data.precipitation,
            )
            db.add(prediction)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
