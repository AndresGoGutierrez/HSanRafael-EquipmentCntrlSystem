# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, get_db  # ✅ importamos Base y get_db desde el módulo correcto
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base de datos de prueba (SQLite temporal)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Configuración del engine y la sesión de prueba
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Fixture para crear y eliminar las tablas antes y después de las pruebas
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ✅ Fixture para obtener una sesión de base de datos aislada en cada test
@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# ✅ Fixture para el cliente de pruebas de FastAPI
@pytest.fixture()
def client():
    # Reemplaza la dependencia de la DB real con la de prueba
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
