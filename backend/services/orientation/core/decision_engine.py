from typing import Dict, Any, List, Optional, Tuple
import logging

from datetime import datetime, timezone # Import timezone
from ..core.config import Settings

logger = logging.getLogger(__name__)

class DecisionEngine:
    """Moteur de décision pour l'orientation des passagers"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.zones = settings.ZONES
        
        # Configuration des contrôles de sécurité
        self.controles_securite = {
            "A": {"temps_moyen": 15, "position": "Terminal 1 - Aile Est", "zone_desservie": ["A", "B"]},
            "B": {"temps_moyen": 20, "position": "Terminal 1 - Centre", "zone_desservie": ["B", "C"]},
            "C": {"temps_moyen": 10, "position": "Terminal 2 - Ouest", "zone_desservie": ["C", "F", "G"]}
        }
    
    def analyser_situation(
        self, 
        meteo_data: Dict[str, Any],
        bagage_data: Dict[str, Any],
        vol_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse la situation globale du passager"""
        
        situation = {
            "type_trajet": "normal",
            "niveau_urgence": "faible",
            "probleme_bagage": False,
            "perturbation_meteo": False,
            "changement_porte": False,
            "temps_disponible": 0,
            "recommandations": []
        }
        
        # Analyse du bagage
        statut_bagage = bagage_data.get("statut", "ENREGISTRE")
        if statut_bagage in ["MAL_ACHEMINE", "EN_VERIFICATION"]:
            situation["probleme_bagage"] = True
            situation["niveau_urgence"] = "eleve"
            situation["type_trajet"] = "probleme_bagage"
            logger.warning(f"Problème bagage détecté: {statut_bagage}")
        
        # Analyse météo
        niveau_alerte_meteo = meteo_data.get("niveau_alerte", "faible")
        if niveau_alerte_meteo != "faible":
            situation["perturbation_meteo"] = True
            if niveau_alerte_meteo == "critique":
                situation["niveau_urgence"] = "critique"
            elif situation["niveau_urgence"] == "faible":
                situation["niveau_urgence"] = "moyen"
        
        # Changement de porte
        porte_originale = vol_data.get("porte_originale")
        porte_actuelle = vol_data.get("porte_actuelle")
        if porte_originale and porte_actuelle and porte_originale != porte_actuelle:
            situation["changement_porte"] = True
            situation["recommandations"].append(
                f"Attention: Changement de porte {porte_originale} → {porte_actuelle}"
            )
        
        # Calcul du temps disponible
        situation["temps_disponible"] = self._calculer_temps_disponible(vol_data)
        
        # Réévaluation de l'urgence basée sur le temps
        if situation["temps_disponible"] < self.settings.TEMPS_CRITIQUE_MIN:
            situation["niveau_urgence"] = "critique"
        elif situation["temps_disponible"] < self.settings.TEMPS_URGENT_MIN:
            if situation["niveau_urgence"] == "faible":
                situation["niveau_urgence"] = "eleve"
        
        logger.info(f"Situation analysée: {situation['niveau_urgence']} - {situation['temps_disponible']}min disponibles")
        
        return situation
    
    def _calculer_temps_disponible(self, vol_data: Dict[str, Any]) -> int:
        """Calcule le temps disponible jusqu'au départ"""
        heure_depart_str = vol_data.get("heure_depart")
        if not heure_depart_str:
            return 90  # Défaut: 90 minutes
        
        heure_depart = datetime.fromisoformat(heure_depart_str.replace('Z', '+00:00'))
        maintenant = datetime.now(timezone.utc) # Use timezone-aware datetime
        temps_disponible = int((heure_depart - maintenant).total_seconds() / 60)
        return max(0, temps_disponible)
    
    def choisir_meilleur_controle(
        self, 
        situation: Dict[str, Any],
        vol_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Choisit le meilleur contrôle de sécurité"""
        
        porte = vol_data.get("porte_actuelle", "A1")
        zone_porte = porte[0]  # Première lettre = zone
        
        # Trouver les contrôles qui desservent cette zone
        controles_possibles = []
        for id_controle, info in self.controles_securite.items():
            if zone_porte in info["zone_desservie"]:
                controles_possibles.append((id_controle, info))
        
        # Si aucun contrôle trouvé, prendre le plus proche
        if not controles_possibles:
            controles_possibles = list(self.controles_securite.items())
        
        # Trier par temps d'attente
        controles_possibles.sort(key=lambda x: x[1]["temps_moyen"])
        
        meilleur_id, meilleur_info = controles_possibles[0]
        
        conseil = ""
        if situation["niveau_urgence"] == "critique":
            conseil = "⚡ Dirigez-vous rapidement vers ce contrôle."
        elif len(controles_possibles) > 1:
            alt_id, alt_info = controles_possibles[1]
            conseil = f"Alternative: Contrôle {alt_id} ({alt_info['temps_moyen']}min)"
        
        return {
            "id": meilleur_id,
            "temps_attente": meilleur_info["temps_moyen"],
            "position": meilleur_info["position"],
            "conseil": conseil,
            "alternative": controles_possibles[1][0] if len(controles_possibles) > 1 else None
        }
    
    def generer_parcours_jitb(
        self,
        situation: Dict[str, Any],
        vol_data: Dict[str, Any],
        position: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Génère un parcours optimisé avec Just-In-Time Boarding"""
        
        etapes = []
        ordre = 1
        
        porte = vol_data.get("porte_actuelle", "A1")
        zone = porte[0]
        temps_restant = situation["temps_disponible"]
        
        # Étape 1: Position actuelle → Sécurité
        if position not in ["zone_embarquement", "porte"]:
            controle = self.choisir_meilleur_controle(situation, vol_data)
            temps_securite = controle["temps_attente"] + 5
            
            etapes.append({
                "ordre": ordre,
                "nom": f"Contrôle de Sécurité {controle['id']}",
                "description": f"Passez le contrôle ({controle['temps_attente']}min d'attente)",
                "zone": f"Sécurité-{controle['id']}",
                "temps_estime": temps_securite,
                "statut": "en_attente"
            })
            ordre += 1
            temps_restant -= temps_securite
        
        # Étape 2: Just-In-Time - Zone d'attente ou direct à la porte
        if temps_restant > 45 and situation["niveau_urgence"] != "critique":
            # Temps de se détendre
            zone_attente = self._trouver_zone_attente_optimale(zone, situation)
            etapes.append({
                "ordre": ordre,
                "nom": f"Zone d'Attente - {zone_attente['nom']}",
                "description": zone_attente["description"],
                "zone": zone_attente["id"],
                "temps_estime": temps_restant - 20,  # Garder 20min pour aller à la porte
                "statut": "en_attente"
            })
            ordre += 1
        
        # Étape 3: Porte d'embarquement
        temps_vers_porte = 15 if situation["niveau_urgence"] == "critique" else 20
        etapes.append({
            "ordre": ordre,
            "nom": f"Porte {porte}",
            "description": f"Embarquement prévu - Arrivée {temps_vers_porte}min avant",
            "zone": zone,
            "temps_estime": temps_vers_porte,
            "statut": "en_attente"
        })
        
        return etapes
    
    def _trouver_zone_attente_optimale(
        self,
        zone_porte: str,
        situation: Dict[str, Any]
    ) -> Dict[str, str]:
        """Trouve la meilleure zone d'attente"""
        
        # Zones d'attente par proximité de porte
        zones_attente = {
            "A": {"id": "lounge-a", "nom": "Salon Business A", "description": "Profitez du salon avec vue sur les pistes"},
            "B": {"id": "commerces-b", "nom": "Galerie Commerciale B", "description": "Restaurants et boutiques à proximité"},
            "C": {"id": "lounge-c", "nom": "Zone de Repos C", "description": "Espace calme avec sièges confortables"},
            "F": {"id": "cafe-f", "nom": "Café Panorama F", "description": "Prenez un café avec vue panoramique"},
            "G": {"id": "restaurant-g", "nom": "Restaurant Terminal G", "description": "Restauration à proximité de votre porte"}
        }
        
        return zones_attente.get(zone_porte, zones_attente["C"])
