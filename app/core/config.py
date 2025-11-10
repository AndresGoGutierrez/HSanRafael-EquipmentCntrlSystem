import os
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import AnyUrl, field_validator
import json


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = False

    DATABASE_URL: AnyUrl

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_CONTAINER_NAME: Optional[str] = None

    EQUIPMENT_MAX_STAY_DAYS: int = 3
    BACKEND_CORS_ORIGINS: List[str] = []

    # Dynamic .env selection
    model_config = SettingsConfigDict(
        env_file=".env.test" if "pytest" in sys.modules else ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before", check_fields=False)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v or []

    @field_validator("DEBUG", mode="before", check_fields=False)
    def parse_debug(cls, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "y")
        return bool(v)


settings = Settings()
