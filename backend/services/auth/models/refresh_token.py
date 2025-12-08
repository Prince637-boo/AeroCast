import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from libs.common.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    token = Column(String, unique=True, index=True, nullable=False)  # hashed token
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

    is_revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def expiry(days=7):
        return datetime.now(timezone.utc) + timedelta(days=days)
