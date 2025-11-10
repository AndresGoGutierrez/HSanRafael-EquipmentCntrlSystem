"""
Test configuration and fixtures.
This file sets up the test environment before pytest loads any tests.
"""

import os
import sys
from pathlib import Path

# Resolve project root dynamically (2 niveles arriba desde este archivo)
project_root = Path(__file__).resolve().parents[1]

# Add project root to PYTHONPATH if not present
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Environment variables used specifically during tests
TEST_ENV_VARS = {
    "DATABASE_URL": "sqlite:///:memory:",  # In-memory DB for fast isolated tests
    "SECRET_KEY": "test-secret-key-for-testing-only",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "AZURE_STORAGE_CONNECTION_STRING": "test-connection-string",
    "AZURE_STORAGE_CONTAINER_NAME": "test-container",
}

# Set environment variables
for key, value in TEST_ENV_VARS.items():
    os.environ.setdefault(key, value)
