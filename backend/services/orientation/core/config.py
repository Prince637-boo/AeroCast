from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    SERVICE_NAME: str = "orientation-service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # URLs des services externes
    METEO_SERVICE_URL: str = "http://meteo-service:8000"
    BAGAGE_SERVICE_URL: str = "http://bagage-service:8000"
    VOL_SERVICE_URL: str = "http://vol-service:8000"
    
    # Configuration aéroport
    AIRPORT_CODE: str = "CDG"
    ZONES: dict = {
        "A": {"portes": ["A1", "A2", "A3", "A4", "A5"], "capacite": 500},
        "B": {"portes": ["B1", "B2", "B3", "B4"], "capacite": 400},
        "C": {"portes": ["C1", "C2", "C3", "C4", "C5", "C6"], "capacite": 600},
        "F": {"portes": ["F10", "F11", "F12"], "capacite": 300},
        "G": {"portes": ["G20", "G21", "G22", "G23", "G24"], "capacite": 550}
    }
    
    # Seuils de temps
    TEMPS_CRITIQUE_MIN: int = 30
    TEMPS_URGENT_MIN: int = 60
    TEMPS_NORMAL_MIN: int = 90
    
    # JWT et sécurité (si nécessaire)
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="ignore"   # ✅ IMPORTANT
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()