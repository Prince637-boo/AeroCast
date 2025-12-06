import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from libs.common.base import Base
from ..core.enums import BaggageStatus

class Baggage(Base):
    __tablename__ = "baggages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    weight = Column(String(50), nullable=True)

    # links
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)

    status = Column(Enum(BaggageStatus), default=BaggageStatus.CHECKED_IN)

    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("BaggageEvent", back_populates="baggage", lazy="selectin")
    
    qr_code_path = Column(String(255), nullable=True)

