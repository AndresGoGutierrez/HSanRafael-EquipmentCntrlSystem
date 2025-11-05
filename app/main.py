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
# Database initialization
# ---------------------------------------------------------------------
def init_database() -> None:
    """Initialize database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)
    


# ---------------------------------------------------------------------
# Storage directory setup
# ---------------------------------------------------------------------
def init_storage() -> None:
    """Ensure storage directories exist for static content"""
    os.makedirs("./storage/equipment-images", exist_ok=True)


# ---------------------------------------------------------------------
# FastAPI application factory
# ---------------------------------------------------------------------
def create_app() -> FastAPI:
    """Application factory to build and configure the FastAPI app"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Sistema de Control de Equipos Hospitalarios - Hospital San Rafael de Tunja",
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

    return app


# ---------------------------------------------------------------------
# Application startup
# ---------------------------------------------------------------------
init_database()
init_storage()
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
