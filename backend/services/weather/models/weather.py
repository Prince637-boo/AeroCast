from sqlalchemy import Column, Integer, Float, DateTime, String
from libs.common.database import Base
from datetime import datetime

class Weather(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)