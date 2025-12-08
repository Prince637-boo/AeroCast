from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    legal_id: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class CompanyOut(BaseModel):
    id: UUID
    name: str
    legal_id: Optional[str]
    contact_email: Optional[EmailStr]

    model_config = ConfigDict(from_attributes=True)
