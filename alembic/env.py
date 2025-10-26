from logging.config import fileConfig
from sqlalchemy import create_engine, pool, engine_from_config
from alembic import context
from app.core.config import settings
from app.core.database import Base

from app.infrastructure.models import UserModel

