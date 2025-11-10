# tests/conftest.py
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# ------------------------------------------------------------
# ✅ Configuración de entorno para permitir imports del proyecto
# ------------------------------------------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ------------------------------------------------------------
# 🧪 Configuración de base de datos de prueba (SQLite temporal)
# ------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------------------------------------------------------------
# 🔹 Fixture de configuración global de la base de datos
# Crea las tablas antes de las pruebas y las elimina al finalizar
# ------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ------------------------------------------------------------
# 🔹 Fixture de sesión aislada para cada prueba
# Permite rollback al finalizar cada test
# ------------------------------------------------------------
@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# ------------------------------------------------------------
# 🔹 Fixture de cliente HTTP para pruebas de FastAPI
# Sobrescribe la dependencia de la base de datos por la de prueba
# ------------------------------------------------------------
@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
