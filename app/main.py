from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import Base, engine
from app.infrastructure import models
from app.presentation.routers import (
    auth_router,
    user_router,
    equipment_router,
    access_control_router,
    audit_router,
    report_router,
)

# ---------------------------------------------------------------------
# Monitoring dependencies
# ---------------------------------------------------------------------
from prometheus_fastapi_instrumentator import Instrumentator


# ---------------------------------------------------------------------
# Database initialization
# ---------------------------------------------------------------------
def init_database() -> None:
    """Initialize database tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------
#                             Storage directory setup
# ---------------------------------------------------------------------
def init_storage() -> None:
    """Ensure storage directories exist for static content."""
    os.makedirs("./storage/equipment-images", exist_ok=True)


# ---------------------------------------------------------------------
#                             FastAPI application factory
# ---------------------------------------------------------------------
def create_app() -> FastAPI:
    """Application factory to build and configure the FastAPI app."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Sistema de Control de Equipos Hospitalarios - Hospital San Rafael de Tunja",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
    )


    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount static files
    app.mount("/storage", StaticFiles(directory="./storage"), name="storage")

    # API Routers
    api_prefix = "/api/v1"
    app.include_router(auth_router.router, prefix=api_prefix)
    app.include_router(user_router.router, prefix=api_prefix)
    app.include_router(equipment_router.router, prefix=api_prefix)
    app.include_router(access_control_router.router, prefix=api_prefix)
    app.include_router(audit_router.router, prefix=api_prefix)
    app.include_router(report_router.router, prefix=api_prefix)

    # Root and Health endpoints
    @app.get("/", tags=["Root"])
    def read_root():
        return {
            "message": "Hospital Equipment Control System API",
            "version": settings.APP_VERSION,
            "status": "active",
        }

    @app.get("/health", tags=["Monitoring"])
    def health_check():
        return {"status": "healthy"}

    # -----------------------------------------------------------------
    # Prometheus Metrics Setup (detailed per-endpoint)
    # -----------------------------------------------------------------
    instrumentator = Instrumentator(
        should_group_status_codes=False,          # Muestra códigos separados (200, 404, etc.)
        should_ignore_untemplated=False,          # Muestra rutas reales (/api/v1/equipment/12)
        excluded_handlers=["/metrics", "/health"] # Ignora métricas internas
    )

    # Instrumenta y expone las métricas
    instrumentator.instrument(app).expose(app, endpoint="/metrics")

    return app


# ---------------------------------------------------------------------
#                             Application startup
# ---------------------------------------------------------------------
init_database()
init_storage()
app = create_app()

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API para control de equipos Hospital San Rafael",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for route in openapi_schema["paths"]:
        for method in openapi_schema["paths"][route]:
            openapi_schema["paths"][route][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
