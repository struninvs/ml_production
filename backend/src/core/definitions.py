import pathlib
from typing import Union, Any

import os

def get_env_variable(var_name: str, default: Union[Any, None] = None) -> str:
    value = os.environ.get(var_name) or default
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return value

ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
SRC_DIR = ROOT_DIR / "src"
DATA_DIR = ROOT_DIR / "backend" / "data"
MODEL_DIR = ROOT_DIR / "backend" / "src" / "models"

BACKEND_HOST = get_env_variable("BACKEND_HOST", "http://dls_trends_indicator_backend")
BACKEND_PORT = get_env_variable("BACKEND_PORT", 8082)