from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field
from enum import Enum

from app.core.settings import settings
from app.api.service_auth_api.main import router_auth
from app.api.service_baggages_api.main import router_baggages
from app.api.service_meteo_ia_api.main import router_meteo_ia

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESC,
    version=settings.PROJECT_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins, 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.include_router(router_auth, prefixe=settings.API_V1_STR)
app.include_router(router_baggages, prefixe=settings.API_V1_STR)
app.include_router(router_meteo_ia, prefixe=settings.API_V1_STR)
