import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timedelta, timezone # Import timezone
from unittest.mock import AsyncMock, patch

from services.orientation.main import app
from services.orientation.core.decision_engine import DecisionEngine
from services.orientation.core.config import Settings
from libs.common.database import get_db
from services.orientation.services.meteo_client import MeteoServiceClient
from services.orientation.services.baggage_client import BagageServiceClient
from services.orientation.services.vol_client import VolServiceClient


@pytest.fixture
async def orientation_client(db_session):
    """Crée un client de test pour l'application d'orientation."""
    app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=app)

    # Mock the service clients directly in the dependency overrides
    mock_meteo_client = AsyncMock(spec=MeteoServiceClient)
    mock_bagage_client = AsyncMock(spec=BagageServiceClient)
    mock_vol_client = AsyncMock(spec=VolServiceClient)

    # Configure default mock return values for successful scenarios
    mock_meteo_client.get_meteo_summary.return_value = {
        "niveau_alerte": "faible", "impact": {}
    }
    mock_bagage_client.get_bagage_status.return_value = {
        "id": "BAG123456", "statut": "EN_SOUTE", "position": "Soute - Avion AF1234"
    }
    mock_vol_client.get_vol_info.return_value = {
        "numero": "AF1234", "destination": "Paris CDG",
        "heure_depart": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
        "porte_originale": "A1", "porte_actuelle": "A1",
        "retard": 0, "statut": "A_L_HEURE", "terminal": "2"
    }

    app.dependency_overrides[MeteoServiceClient] = lambda: mock_meteo_client
    app.dependency_overrides[BagageServiceClient] = lambda: mock_bagage_client
    app.dependency_overrides[VolServiceClient] = lambda: mock_vol_client

    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
@pytest.mark.asyncio
class TestOrientationAPI:
    """Tests pour l'API d'orientation"""
    
    async def test_health_check(self, orientation_client: AsyncClient):
        """Test du endpoint de santé"""
        response = await orientation_client.get("/api/orientation/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    async def test_root(self, orientation_client: AsyncClient):
        """Test du endpoint racine"""
        response = await orientation_client.get("/")
        assert response.status_code == 200
        assert "service" in response.json()
    
    async def test_get_orientation_success(self, orientation_client: AsyncClient):
        """Test réussi de récupération d'orientation"""
        # The mocks are now configured in the orientation_client fixture
        # We can directly access the mocked clients via dependency overrides if needed for specific test cases
        # For this test, we'll just use the default mocked values set in the fixture.

        # Override specific mock return values for this test if needed
        mock_meteo_client = app.dependency_overrides[MeteoServiceClient]()
        mock_bagage_client = app.dependency_overrides[BagageServiceClient]()
        mock_vol_client = app.dependency_overrides[VolServiceClient]()

        mock_meteo_client.get_meteo_summary.return_value = {
            "niveau_alerte": "moyen",
            "impact": {
                "capacite_horaire_reduite": 0.2,
                "retard_moyen": 15,
                "secteurs_congestionnes": ["G"]
            }
        }
        mock_vol_client.get_vol_info.return_value = {
            "numero": "AF1234",
            "destination": "Paris CDG",
            "heure_depart": (datetime.now(timezone.utc) + timedelta(hours=1, minutes=30)).isoformat(),
            "porte_originale": "G24",
            "porte_actuelle": "F12",
            "retard": 15,
            "statut": "RETARDE",
            "terminal": "2"
        }

        # Appel de l'API
        response = await orientation_client.get("/api/orientation/AF1234/BAG123456")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["numero_vol"] == "AF1234"
        assert "instructions" in data
        assert "alertes" in data
        assert "parcours" in data
    
    async def test_get_orientation_invalid_vol(self, orientation_client: AsyncClient):
        """Test avec un numéro de vol invalide"""
        response = await orientation_client.get("/api/orientation/AB/BAG123456")
        assert response.status_code == 400
    
    async def test_get_orientation_invalid_bagage(self, orientation_client: AsyncClient):
        """Test avec un ID bagage invalide"""
        response = await orientation_client.get("/api/orientation/AF1234/AB")
        assert response.status_code == 400
    
    async def test_post_orientation(self, orientation_client: AsyncClient):
        """Test de l'endpoint POST"""
        # The mocks are now configured in the orientation_client fixture
        # For this test, we'll just use the default mocked values set in the fixture.

        payload = {
            "numero_vol": "AF1234",
            "id_bagage": "BAG123456",
            "position_estimee": "entree"
        }
        response = await orientation_client.post("/api/orientation/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["numero_vol"] == "AF1234"


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
            "heure_depart": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
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
        vol_data = { # Use timezone-aware datetime
            "heure_depart": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
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
        vol_data = { # Use timezone-aware datetime
            "heure_depart": (datetime.now(timezone.utc) + timedelta(minutes=25)).isoformat(),
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
