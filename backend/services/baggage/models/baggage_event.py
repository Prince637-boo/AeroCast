import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from libs.common.base import Base
from ..core.enums import BaggageStatus

class BaggageEvent(Base):
    __tablename__ = "baggage_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    baggage_id = Column(UUID(as_uuid=True), ForeignKey("baggages.id"))
    status = Column(Enum(BaggageStatus))
    location = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)

    baggage = relationship("Baggage", back_populates="events")
