from fastapi import FastAPI

from libs.common.database import engine
from .otel_setup import init_tracing

from .routers.baggages import router as baggage_router
from .routers.admin import router as admin_router
from .routers.ws import router as ws_router
from .routers.gps import router as gps_router
from .routers.trackers import router as trackers_router

# -------------------------------
# INITIALISATION DE L'APPLICATION
# -------------------------------
app = FastAPI(
    title="Service de Traçage des Baggages",
    description="""
    Service backend pour le suivi des bagages en temps réel.
    """,
    version="1.0.0",
)

# -------------------------------
# INITIALISATION OPENTELEMETRY
# -------------------------------
# Permet de tracer toutes les requêtes et opérations pour monitoring/observabilité
init_tracing(app, db_engine=engine)

# -------------------------------
# INCLUSION DES ROUTERS
# -------------------------------
# Router pour les routes publiques (passager/compagnie)
app.include_router(baggage_router)

# Router pour les routes admin
app.include_router(admin_router)

# Router pour les WebSocket (temps réel)
app.include_router(ws_router)

app.include_router(gps_router)
app.include_router(trackers_router)

# -------------------------------
# POINTS D'EXTENSION
# -------------------------------
# Ici, on peut ajouter des événements startup/shutdown, middleware global, etc.
# Exemple :
# @app.on_event("startup")
# async def on_startup():
#     print("Application démarrée")
