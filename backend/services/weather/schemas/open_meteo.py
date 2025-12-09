from pydantic import BaseModel

class CurrentWeather(BaseModel):
    temperature: float
    windspeed: float
    weathercode: int
    time: str

class OpenMeteoResponse(BaseModel):
    latitude: float
    longitude: float
    current_weather: CurrentWeather