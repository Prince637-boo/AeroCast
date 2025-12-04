import enum
import uuid

from sqlalchemy import UUID, Column, String, Integer, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.core.config import Base


class RoleUtilisateur(str, enum.Enum):
    PASSAGER = "PASSAGER"
    COMPAGNIE = "COMPAGNIE"
    ATC = "ATC"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(128), nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)

    role = Column(Enum(RoleUtilisateur), nullable=False, default=RoleUtilisateur.PASSAGER)

    id_compagnie = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"

    @property
    def est_admin(self) -> bool:
        return self.role == RoleUtilisateur.ADMIN

    @property
    def est_compagnie(self) -> bool:
        return self.role == RoleUtilisateur.COMPAGNIE

    @property
    def est_atc(self) -> bool:
        return self.role == RoleUtilisateur.ATC
