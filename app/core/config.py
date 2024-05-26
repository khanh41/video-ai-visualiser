"""Define config for project."""
from __future__ import annotations

import logging
import sys

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

API_PREFIX = "/api"

VERSION = "0.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

APP_HOST: str = config("APP_HOST", cast=str, default="127.0.0.1")
APP_PORT: str = config("APP_PORT", cast=str, default="8000")

PROJECT_NAME: str = config("PROJECT_NAME", default="Video AI Visualiser")
ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="")
TRITON_SERVER_URL: str = config("TRITON_SERVER_URL", cast=str, default="localhost:8001")

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
