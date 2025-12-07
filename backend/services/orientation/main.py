from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from core.config import get_settings
from routers import orientation
from middleware.logging import setup_logging

# Configuration du logging
setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    logger.info(f"🚀 Démarrage du service {settings.SERVICE_NAME} v{settings.VERSION}")
    yield
    logger.info("🛑 Arrêt du service")


# Création de l'application
app = FastAPI(
    title="MODP - Mécanisme d'Orientation Dynamique des Passagers",
    description="Service d'orientation intelligente des passagers basé sur l'IA Météo et la traçabilité bagages",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(orientation.router)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint racine"""
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Endpoint de santé global"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION
    }
