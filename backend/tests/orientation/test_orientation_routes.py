import pytest
import pytest_asyncio
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from httpx import ASGITransport, AsyncClient

from services.orientation.main import app
from services.orientation.core.decision_engine import DecisionEngine
from services.orientation.core.config import Settings


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestOrientationAPI:
    """Tests pour l'API d'orientation"""

    @pytest.mark.asyncio
    async def test_health_check(self, client):
        response = await client.get("/api/orientation/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_root(self, client):
        response = await client.get("/")
        assert response.status_code == 200
        assert "service" in response.json()

    @pytest.mark.asyncio
    async def test_get_orientation_success(self, client):
        """Test réussi de récupération d'orientation"""
        with patch('services.orientation.routers.orientation.services.meteo_client') as mock_meteo, \
             patch('services.orientation.routers.orientation.services.baggage_client') as mock_bagage, \
             patch('services.orientation.routers.orientation.services.vol_client') as mock_vol:

            # --- AsyncMock pour chaque client ---
            mock_meteo_instance = AsyncMock()
            mock_meteo_instance.get_meteo_summary.return_value = {
                "niveau_alerte": "moyen",
                "impact": {
                    "capacite_horaire_reduite": 0.2,
                    "retard_moyen": 15,
                    "secteurs_congestionnes": ["G"]
                }
            }
            mock_meteo.return_value = mock_meteo_instance

            mock_bagage_instance = AsyncMock()
            mock_bagage_instance.get_bagage_status.return_value = {
                "id": "BAG123456",
                "statut": "EN_SOUTE",
                "position": "Soute - Avion AF1234"
            }
            mock_bagage.return_value = mock_bagage_instance

            mock_vol_instance = AsyncMock()
            mock_vol_instance.get_vol_info.return_value = {
                "numero": "AF1234",
                "destination": "Paris CDG",
                "heure_depart": (datetime.now() + timedelta(hours=1, minutes=30)).isoformat(),
                "porte_originale": "G24",
                "porte_actuelle": "F12",
                "retard": 15,
                "statut": "RETARDE",
                "terminal": "2"
            }
            mock_vol.return_value = mock_vol_instance
            # --- Fin AsyncMock ---

            response = await client.get("/api/orientation/AF1234/BAG123456")

            print("skdfks")
            data = response.json()
            print(data)
            assert response.status_code == 200
            assert data["success"] is True
            assert data["numero_vol"] == "AF1234"
            assert "instructions" in data
            assert "alertes" in data
            assert "parcours" in data

    @pytest.mark.asyncio
    async def test_get_orientation_invalid_vol(self, client):
        """Test avec un numéro de vol invalide"""
        response = await client.get("/api/orientation/AB/BAG123456")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_get_orientation_invalid_bagage(self, client):
        """Test avec un ID bagage invalide"""
        response = await client.get("/api/orientation/AF1234/AB")
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_post_orientation(self, client):
        """Test de l'endpoint POST avec services mockés"""
        with patch('services.orientation.routers.orientation.get_meteo_client') as mock_meteo, \
             patch('services.orientation.routers.orientation.get_bagage_client') as mock_bagage, \
             patch('services.orientation.routers.orientation.get_vol_client') as mock_vol:

            # --- AsyncMock pour chaque client ---
            mock_meteo_instance = AsyncMock()
            mock_meteo_instance.get_meteo_summary.return_value = {
                "niveau_alerte": "faible",
                "impact": {"capacite_horaire_reduite": 0.0}
            }
            mock_meteo.return_value = mock_meteo_instance

            mock_bagage_instance = AsyncMock()
            mock_bagage_instance.get_bagage_status.return_value = {
                "id": "BAG123456",
                "statut": "EN_SOUTE",
                "position": "Soute - Avion AF1234"
            }
            mock_bagage.return_value = mock_bagage_instance

            mock_vol_instance = AsyncMock()
            mock_vol_instance.get_vol_info.return_value = {
                "numero": "AF1234",
                "destination": "Paris CDG",
                "heure_depart": (datetime.now() + timedelta(hours=2)).isoformat(),
                "porte_originale": "G24",
                "porte_actuelle": "F12",
                "retard": 0,
                "statut": "A_HEURE",
                "terminal": "2"
            }
            mock_vol.return_value = mock_vol_instance
            # --- Fin AsyncMock ---

            payload = {
                "numero_vol": "AF1234",
                "id_bagage": "BAG123456",
                "position_estimee": "entree"
            }

            response = await client.post("/api/orientation/", json=payload)

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "instructions" in data
            assert "alertes" in data
            assert "parcours" in data


class TestDecisionEngine:
    """Tests pour le moteur de décision"""

    @pytest.fixture
    def settings(self):
        return Settings()

    @pytest.fixture
    def engine(self, settings):
        return DecisionEngine(settings)

    def test_analyser_situation_normal(self, engine):
        meteo_data = {"niveau_alerte": "faible", "impact": {"capacite_horaire_reduite": 0.0}}
        bagage_data = {"statut": "EN_SOUTE"}
        vol_data = {"heure_depart": (datetime.now() + timedelta(hours=2)).isoformat(),
                    "porte_originale": "A1",
                    "porte_actuelle": "A1"}

        situation = engine.analyser_situation(meteo_data, bagage_data, vol_data)
        assert situation["niveau_urgence"] == "faible"
        assert situation["probleme_bagage"] is False
        assert situation["perturbation_meteo"] is False
        assert situation["changement_porte"] is False

    def test_analyser_situation_bagage_probleme(self, engine):
        meteo_data = {"niveau_alerte": "faible", "impact": {}}
        bagage_data = {"statut": "MAL_ACHEMINE"}
        vol_data = {"heure_depart": (datetime.now() + timedelta(hours=2)).isoformat(),
                    "porte_originale": "A1",
                    "porte_actuelle": "A1"}

        situation = engine.analyser_situation(meteo_data, bagage_data, vol_data)
        assert situation["probleme_bagage"] is True
        assert situation["niveau_urgence"] == "eleve"
        assert situation["type_trajet"] == "probleme_bagage"

    def test_analyser_situation_critique(self, engine):
        meteo_data = {"niveau_alerte": "faible", "impact": {}}
        bagage_data = {"statut": "EN_SOUTE"}
        vol_data = {"heure_depart": (datetime.now() + timedelta(minutes=25)).isoformat(),
                    "porte_originale": "A1",
                    "porte_actuelle": "A1"}

        situation = engine.analyser_situation(meteo_data, bagage_data, vol_data)
        assert situation["niveau_urgence"] == "critique"
        assert situation["temps_disponible"] < 30

    def test_choisir_meilleur_controle(self, engine):
        situation = {"niveau_urgence": "moyen"}
        vol_data = {"porte_actuelle": "C5"}
        controle = engine.choisir_meilleur_controle(situation, vol_data)
        assert "id" in controle
        assert "temps_attente" in controle
        assert "position" in controle
        assert controle["id"] in ["A", "B", "C"]

    def test_generer_parcours_jitb_normal(self, engine):
        situation = {"niveau_urgence": "faible", "temps_disponible": 90}
        vol_data = {"porte_actuelle": "A1"}
        position = "entree"
        parcours = engine.generer_parcours_jitb(situation, vol_data, position)
        assert len(parcours) >= 2
        assert all("ordre" in etape for etape in parcours)
        assert all("temps_estime" in etape for etape in parcours)

    def test_generer_parcours_jitb_urgent(self, engine):
        situation = {"niveau_urgence": "critique", "temps_disponible": 25}
        vol_data = {"porte_actuelle": "G24"}
        position = "entree"
        parcours = engine.generer_parcours_jitb(situation, vol_data, position)
        assert not any("Zone d'Attente" in etape.get("nom", "") for etape in parcours)
