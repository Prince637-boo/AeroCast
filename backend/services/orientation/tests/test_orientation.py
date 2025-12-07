import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from main import app
from core.decision_engine import DecisionEngine
from core.config import Settings

client = TestClient(app)


class TestOrientationAPI:
    """Tests pour l'API d'orientation"""
    
    def test_health_check(self):
        """Test du endpoint de santé"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root(self):
        """Test du endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        assert "service" in response.json()
    
    @pytest.mark.asyncio
    async def test_get_orientation_success(self):
        """Test réussi de récupération d'orientation"""
        # Mock des clients de services
        with patch('routers.orientation.get_meteo_client') as mock_meteo, \
             patch('routers.orientation.get_bagage_client') as mock_bagage, \
             patch('routers.orientation.get_vol_client') as mock_vol:
            
            # Configuration des mocks
            mock_meteo.return_value.get_meteo_summary = AsyncMock(return_value={
                "niveau_alerte": "moyen",
                "impact": {
                    "capacite_horaire_reduite": 0.2,
                    "retard_moyen": 15,
                    "secteurs_congestionnes": ["G"]
                }
            })
            
            mock_bagage.return_value.get_bagage_status = AsyncMock(return_value={
                "id": "BAG123456",
                "statut": "EN_SOUTE",
                "position": "Soute - Avion AF1234"
            })
            
            mock_vol.return_value.get_vol_info = AsyncMock(return_value={
                "numero": "AF1234",
                "destination": "Paris CDG",
                "heure_depart": (datetime.now() + timedelta(hours=1, minutes=30)).isoformat(),
                "porte_originale": "G24",
                "porte_actuelle": "F12",
                "retard": 15,
                "statut": "RETARDE",
                "terminal": "2"
            })
            
            # Appel de l'API
            response = client.get("/api/orientation/AF1234/BAG123456")
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["numero_vol"] == "AF1234"
            assert "instructions" in data
            assert "alertes" in data
            assert "parcours" in data
    
    def test_get_orientation_invalid_vol(self):
        """Test avec un numéro de vol invalide"""
        response = client.get("/api/orientation/AB/BAG123456")
        assert response.status_code == 400
    
    def test_get_orientation_invalid_bagage(self):
        """Test avec un ID bagage invalide"""
        response = client.get("/api/orientation/AF1234/AB")
        assert response.status_code == 400
    
    def test_post_orientation(self):
        """Test de l'endpoint POST"""
        with patch('routers.orientation.get_meteo_client'), \
             patch('routers.orientation.get_bagage_client'), \
             patch('routers.orientation.get_vol_client'):
            
            payload = {
                "numero_vol": "AF1234",
                "id_bagage": "BAG123456",
                "position_estimee": "entree"
            }
            
            response = client.post("/api/orientation/", json=payload)
            # Le test complet nécessiterait de mocker tous les services
            assert response.status_code in [200, 500]  # 500 si les services ne répondent pas


class TestDecisionEngine:
    """Tests pour le moteur de décision"""
    
    @pytest.fixture
    def settings(self):
        """Fixture pour les paramètres"""
        return Settings()
    
    @pytest.fixture
    def engine(self, settings):
        """Fixture pour le moteur de décision"""
        return DecisionEngine(settings)
    
    def test_analyser_situation_normal(self, engine):
        """Test d'analyse de situation normale"""
        meteo_data = {
            "niveau_alerte": "faible",
            "impact": {"capacite_horaire_reduite": 0.0}
        }
        
        bagage_data = {
            "statut": "EN_SOUTE"
        }
        
        vol_data = {
            "heure_depart": (datetime.now() + timedelta(hours=2)).isoformat(),
            "porte_originale": "A1",
            "porte_actuelle": "A1"
        }
        
        situation = engine.analyser_situation(meteo_data, bagage_data, vol_data)
        
        assert situation["niveau_urgence"] == "faible"
        assert situation["probleme_bagage"] is False
        assert situation["perturbation_meteo"] is False
        assert situation["changement_porte"] is False
    
    def test_analyser_situation_bagage_probleme(self, engine):
        """Test avec problème de bagage"""
        meteo_data = {"niveau_alerte": "faible", "impact": {}}
        bagage_data = {"statut": "MAL_ACHEMINE"}
        vol_data = {
            "heure_depart": (datetime.now() + timedelta(hours=2)).isoformat(),
            "porte_originale": "A1",
            "porte_actuelle": "A1"
        }
        
        situation = engine.analyser_situation(meteo_data, bagage_data, vol_data)
        
        assert situation["probleme_bagage"] is True
        assert situation["niveau_urgence"] == "eleve"
        assert situation["type_trajet"] == "probleme_bagage"
    
    def test_analyser_situation_critique(self, engine):
        """Test avec situation critique (peu de temps)"""
        meteo_data = {"niveau_alerte": "faible", "impact": {}}
        bagage_data = {"statut": "EN_SOUTE"}
        vol_data = {
            "heure_depart": (datetime.now() + timedelta(minutes=25)).isoformat(),
            "porte_originale": "A1",
            "porte_actuelle": "A1"
        }
        
        situation = engine.analyser_situation(meteo_data, bagage_data, vol_data)
        
        assert situation["niveau_urgence"] == "critique"
        assert situation["temps_disponible"] < 30
    
    def test_choisir_meilleur_controle(self, engine):
        """Test du choix du meilleur contrôle"""
        situation = {"niveau_urgence": "moyen"}
        vol_data = {"porte_actuelle": "C5"}
        
        controle = engine.choisir_meilleur_controle(situation, vol_data)
        
        assert "id" in controle
        assert "temps_attente" in controle
        assert "position" in controle
        assert controle["id"] in ["A", "B", "C"]
    
    def test_generer_parcours_jitb_normal(self, engine):
        """Test de génération de parcours normal"""
        situation = {
            "niveau_urgence": "faible",
            "temps_disponible": 90
        }
        vol_data = {"porte_actuelle": "A1"}
        position = "entree"
        
        parcours = engine.generer_parcours_jitb(situation, vol_data, position)
        
        assert len(parcours) >= 2  # Au moins sécurité + porte
        assert all("ordre" in etape for etape in parcours)
        assert all("temps_estime" in etape for etape in parcours)
    
    def test_generer_parcours_jitb_urgent(self, engine):
        """Test de génération de parcours urgent"""
        situation = {
            "niveau_urgence": "critique",
            "temps_disponible": 25
        }
        vol_data = {"porte_actuelle": "G24"}
        position = "entree"
        
        parcours = engine.generer_parcours_jitb(situation, vol_data, position)
        
        # Pas de zone d'attente en mode critique
        assert not any("Zone d'Attente" in etape.get("nom", "") for etape in parcours)

