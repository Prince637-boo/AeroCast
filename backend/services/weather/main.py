from fastapi import FastAPI, Depends
from .models.prediction import fetch_weather_data, parse_weather_data
from .models.database import SessionLocal, WeatherPrediction
from .schemas.weather import WeatherData
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/weather/{latitude}/{longitude}", response_model=WeatherData)
def get_weather(latitude: float, longitude: float, db: Session = Depends(get_db)):
    raw_data = fetch_weather_data(latitude, longitude)
    weather_data = parse_weather_data(raw_data)
    # Sauvegarde en base
    prediction = WeatherPrediction(
        latitude=latitude,
        longitude=longitude,
        temperature=weather_data.temperature,
        humidity=weather_data.humidity,
        wind_speed=weather_data.wind_speed,
        precipitation=weather_data.precipitation,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return weather_data

@app.get("/weather/history", response_model=List[WeatherPrediction])
def get_weather_history(db: Session = Depends(get_db)):
    return db.query(WeatherPrediction).all()
