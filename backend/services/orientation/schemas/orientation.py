from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TypeInstruction(str, Enum):
    NORMAL = "NORMAL"
    URGENT = "URGENT"
    CRITIQUE = "CRITIQUE"
    INFO = "INFO"

class ActionType(str, Enum):
    SE_RENDRE = "SE_RENDRE"
    PASSER_SECURITE = "PASSER_SECURITE"
    ATTENDRE = "ATTENDRE"
    EMBARQUER = "EMBARQUER"
    CONTACTER_SERVICE = "CONTACTER_SERVICE"

class InstructionSchema(BaseModel):
    priorite: int = Field(..., ge=1, description="Priorité de l'instruction")
    type: TypeInstruction
    action: ActionType
    destination: str
    description: str
    temps_estime: int = Field(..., description="Temps estimé en minutes")
    icon: str
    details: Optional[Dict[str, Any]] = None

class AlerteSchema(BaseModel):
    niveau: str = Field(..., description="Niveau d'alerte: info, warning, danger")
    message: str
    icon: str
    action_recommandee: Optional[str] = None

class EtapeParcoursSchema(BaseModel):
    ordre: int
    nom: str
    description: str
    zone: str
    temps_estime: int
    statut: str = Field(..., description="en_attente, en_cours, termine")
    coordonnees: Optional[Dict[str, float]] = None

class SituationSchema(BaseModel):
    type_trajet: str
    niveau_urgence: str
    probleme_bagage: bool
    perturbation_meteo: bool
    changement_porte: bool
    temps_disponible: int
    recommandations: List[str] = []

class OrientationRequest(BaseModel):
    numero_vol: str = Field(..., min_length=5, max_length=10)
    id_bagage: str = Field(..., min_length=5)
    position_estimee: Optional[str] = Field(None, description="entree, securite, zone_embarquement, porte")
    
    @validator('numero_vol')
    def validate_numero_vol(cls, v):
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Numéro de vol invalide')
        return v.upper()

class OrientationResponse(BaseModel):
    success: bool
    numero_vol: str
    timestamp: datetime
    situation: SituationSchema
    instructions: List[InstructionSchema]
    alertes: List[AlerteSchema]
    parcours: List[EtapeParcoursSchema]
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "numero_vol": "AF1234",
                "timestamp": "2025-12-07T10:30:00Z",
                "situation": {
                    "type_trajet": "normal",
                    "niveau_urgence": "moyen",
                    "probleme_bagage": False,
                    "perturbation_meteo": True,
                    "changement_porte": True,
                    "temps_disponible": 65,
                    "recommandations": ["Prenez le contrôle C pour gagner du temps"]
                },
                "instructions": [],
                "alertes": [],
                "parcours": []
            }
        }