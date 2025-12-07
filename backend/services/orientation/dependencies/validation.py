from fastapi import HTTPException, status
from typing import Optional

class OrientationValidator:
    """Validateur pour les requêtes d'orientation"""
    
    @staticmethod
    def validate_numero_vol(numero_vol: str) -> str:
        """Valide le format du numéro de vol"""
        if not numero_vol or len(numero_vol) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Numéro de vol invalide"
            )
        return numero_vol.upper().strip()
    
    @staticmethod
    def validate_id_bagage(id_bagage: str) -> str:
        """Valide le format de l'ID bagage"""
        if not id_bagage or len(id_bagage) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID bagage invalide"
            )
        return id_bagage.strip()
    
    @staticmethod
    def validate_position(position: Optional[str]) -> Optional[str]:
        """Valide la position estimée"""
        positions_valides = ["entree", "securite", "zone_embarquement", "porte", None]
        if position and position not in positions_valides:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Position invalide. Valeurs acceptées: {', '.join(filter(None, positions_valides))}"
            )
        return position
