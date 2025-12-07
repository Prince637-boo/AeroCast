from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class NiveauUrgence(str, enum.Enum):
    FAIBLE = "faible"
    MOYEN = "moyen"
    ELEVE = "eleve"
    CRITIQUE = "critique"

class StatutBagage(str, enum.Enum):
    ENREGISTRE = "ENREGISTRE"
    EN_SOUTE = "EN_SOUTE"
    MAL_ACHEMINE = "MAL_ACHEMINE"
    EN_VERIFICATION = "EN_VERIFICATION"

class OrientationLog(Base):
    __tablename__ = "orientation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_vol = Column(String, index=True, nullable=False)
    id_bagage = Column(String, index=True, nullable=False)
    position_estimee = Column(String, nullable=True)
    
    # Résultat de l'orientation
    niveau_urgence = Column(Enum(NiveauUrgence), nullable=False)
    instructions = Column(JSON, nullable=False)
    parcours = Column(JSON, nullable=False)
    alertes = Column(JSON, nullable=True)
    
    # Contexte
    impact_meteo = Column(JSON, nullable=True)
    statut_bagage = Column(Enum(StatutBagage), nullable=False)
    temps_disponible = Column(Integer, nullable=False)  # en minutes
    
    # Métadonnées
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
