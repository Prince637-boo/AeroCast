from fastapi import FastAPI

from libs.common.database import engine
from .otel_setup import init_tracing

from .routers.baggages import router as baggage_router
from .routers.admin import router as admin_router
from .routers.ws import router as ws_router

app = FastAPI(title="Baggage Tracking Service")

# ---- INITIALISATION OPENTELEMETRY AU DÉMARRAGE ----
init_tracing(app, db_engine=engine)

# ROUTES
app.include_router(baggage_router)
app.include_router(admin_router)
app.include_router(ws_router)
