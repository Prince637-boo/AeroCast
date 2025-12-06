from pydantic import BaseModel
from typing import Optional
from ..core.enums import BaggageStatus

class BaggageEventCreate(BaseModel):
    status: BaggageStatus
    location: str

class BaggageEventOut(BaseModel):
    id: str
    status: BaggageStatus
    location: str
    timestamp: str

    class Config:
        from_attributes = True
