iimport os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Open-Meteo
    WEATHER_API_URL: str = os.getenv("WEATHER_API_URL", "https://api.open-meteo.com/v1/forecast")

    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5433/weather_db")

    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "pyamqp://admin:admin@rabbitmq//")
    CELERY_BEAT_SCHEDULE: dict = {
        'fetch-and-save-weather': {
            'task': 'services.weather.workers.tasks.fetch_and_save_weather',
            'schedule': 3600.0,  # Exécute toutes les heures (en secondes)
        }
    }

settings = Settings()

