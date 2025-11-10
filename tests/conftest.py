import os
import sys

# Add the project root to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return TestClient(app)