from asyncio.log import logger
from typing import Optional
from .core.decision_engine import DecisionEngine
from .schemas.orientation import ActionType, TypeInstruction


def generer_instructions(
    decision_engine: DecisionEngine,
    situation: dict,
    position_estimee: Optional[str],
    vol_data: dict,
    bagage_data: dict
) -> list:
    """Génère les instructions personnalisées"""
    instructions = []
    
    # Cas 1: Problème de bagage - Priorité absolue
    if situation["probleme_bagage"]:
        instructions.append({
            "priorite": 1,
            "type": TypeInstruction.CRITIQUE,
            "action": ActionType.CONTACTER_SERVICE,
            "destination": "Bureau Service Bagages - Terminal 2, Zone C",
            "description": f"Votre bagage est {bagage_data['statut']}. Veuillez vous rendre immédiatement au bureau des services bagages.",
            "temps_estime": 10,
            "icon": "alert-circle",
            "details": {
                "telephone": "+33 1 XX XX XX XX",
                "horaires": "24/7"
            }
        })
        return instructions
    
    priorite = 1
    
    # Cas 2: Contrôle de sécurité
    if position_estimee not in ["zone_embarquement", "porte"]:
        controle = decision_engine.choisir_meilleur_controle(situation, vol_data)
        
        type_instruction = TypeInstruction.URGENT if situation["niveau_urgence"] == "critique" else TypeInstruction.NORMAL
        
        instructions.append({
            "priorite": priorite,
            "type": type_instruction,
            "action": ActionType.PASSER_SECURITE,
            "destination": f"Contrôle de Sécurité {controle['id']}",
            "description": f"Temps d'attente estimé: {controle['temps_attente']} minutes. {controle['conseil']}",
            "temps_estime": controle["temps_attente"] + 5,
            "icon": "shield-check",
            "details": {
                "position": controle["position"],
                "alternative": controle.get("alternative")
            }
        })
        priorite += 1
    
    # Cas 3: Zone d'attente (JITB)
    if situation["temps_disponible"] > 45 and situation["niveau_urgence"] != "critique":
        zone = vol_data.get("porte_actuelle", "A1")[0]
        zone_attente = decision_engine._trouver_zone_attente_optimale(zone, situation)
        
        instructions.append({
            "priorite": priorite,
            "type": TypeInstruction.INFO,
            "action": ActionType.ATTENDRE,
            "destination": zone_attente["nom"],
            "description": f"{zone_attente['description']} Vous serez notifié quand il sera temps de vous diriger vers la porte.",
            "temps_estime": situation["temps_disponible"] - 25,
            "icon": "coffee",
            "details": {
                "zone_id": zone_attente["id"],
                "amenites": ["WiFi gratuit", "Prises électriques", "Toilettes"]
            }
        })
        priorite += 1
    
    # Cas 4: Porte d'embarquement
    porte = vol_data.get("porte_actuelle", "A1")
    temps_avant_porte = 15 if situation["niveau_urgence"] == "critique" else 20
    
    type_final = TypeInstruction.URGENT if situation["niveau_urgence"] in ["critique", "eleve"] else TypeInstruction.NORMAL
    
    instructions.append({
        "priorite": priorite,
        "type": type_final,
        "action": ActionType.EMBARQUER,
        "destination": f"Porte {porte}",
        "description": f"Présentez-vous à la porte {temps_avant_porte} minutes avant le départ.",
        "temps_estime": temps_avant_porte,
        "icon": "plane",
        "details": {
            "porte": porte,
            "terminal": vol_data.get("terminal", "2"),
            "embarquement_prevu": vol_data.get("heure_depart")
        }
    })
    
    return instructions


def generer_alertes(situation: dict, meteo_data: dict, vol_data: dict) -> list:
    """Génère les alertes contextuelles"""
    alertes = []
    
    # Alerte changement de porte
    if situation["changement_porte"]:
        alertes.append({
            "niveau": "warning",
            "message": f"Changement de porte: {vol_data['porte_originale']} → {vol_data['porte_actuelle']}",
            "icon": "alert-triangle",
            "action_recommandee": "Vérifiez les écrans d'information"
        })
    
    # Alerte météo
    if situation["perturbation_meteo"]:
        niveau_alerte = meteo_data.get("niveau_alerte", "moyen")
        conditions = meteo_data.get("impact", {}).get("conditions", [])
        
        if niveau_alerte == "critique":
            alertes.append({
                "niveau": "danger",
                "message": f"Alerte météo critique: {', '.join(conditions)}. Retards importants attendus.",
                "icon": "cloud-lightning",
                "action_recommandee": "Restez informé via l'application"
            })
        else:
            alertes.append({
                "niveau": "info",
                "message": f"Conditions météo dégradées: {', '.join(conditions)}. Légers retards possibles.",
                "icon": "cloud",
                "action_recommandee": None
            })
    
    # Alerte temps critique
    if situation["niveau_urgence"] == "critique":
        alertes.append({
            "niveau": "danger",
            "message": f"Temps limité: {situation['temps_disponible']} minutes avant le départ!",
            "icon": "clock",
            "action_recommandee": "Dirigez-vous immédiatement vers votre porte"
        })
    elif situation["niveau_urgence"] == "eleve":
        alertes.append({
            "niveau": "warning",
            "message": f"Embarquement proche: {situation['temps_disponible']} minutes restantes",
            "icon": "clock",
            "action_recommandee": "Ne tardez pas"
        })
    
    return alertes


async def log_orientation(
    numero_vol: str,
    id_bagage: str,
    situation: dict,
    instructions: list
):
    """Log l'orientation en arrière-plan (optionnel)"""
    logger.info(
        f"Orientation calculée - Vol: {numero_vol}, "
        f"Bagage: {id_bagage}, "
        f"Urgence: {situation['niveau_urgence']}, "
        f"Instructions: {len(instructions)}"
    )
    