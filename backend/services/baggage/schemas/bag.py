from pydantic import BaseModel
from typing import Optional
from ..core.enums import BaggageStatus

class BaggageCreate(BaseModel):
    owner_id: str
    company_id: str
    description: Optional[str] = None
    weight: Optional[str] = None

class BaggageOut(BaseModel):
    id: str
    tag: str
    qr_code_path: str | None
    description: Optional[str]
    weight: Optional[str]
    status: BaggageStatus

    class Config:
        from_attributes = True

