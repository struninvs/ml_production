from typing import Literal

from pydantic import IPvAnyAddress
from pydantic_settings import BaseSettings

from core.definitions import BACKEND_PORT


class Settings(BaseSettings):
    APP_NAME: str = "WorkshopDLS"
    APP_HOST: IPvAnyAddress = "0.0.0.0"  # type: ignore
    APP_PORT: int = int(BACKEND_PORT)

    VERSION: Literal["dev", "prod"] = "dev"
    DEBUG: bool = False
    DEVELOPMENT: bool = False
    LOGLEVEL: str = "WARNING"