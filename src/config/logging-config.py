from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIR = Path(
    os.getenv(
        "LOG_DIR",
        str(PROJECT_ROOT / "logs"),
    )
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIR / os.getenv(
    "LOG_FILE",
    "payment-ai.log",
)

ERROR_LOG_FILE = LOG_DIR / os.getenv(
    "ERROR_LOG_FILE",
    "payment-ai-error.log",
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()

# =====================================================
# Logging Configuration
# =====================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setuplog() -> None:
    """
    Configure application logging.

    This method should be called once during application startup.
    """

    root_logger = logging.getLogger()

    # Prevent duplicate handlers
    if root_logger.handlers:
        return

    root_logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # -------------------------------------------------
    # Console Handler
    # -------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    # -------------------------------------------------
    # Application Log
    # -------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=10 * 1024 * 1024,   # 10 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # -------------------------------------------------
    # Error Log
    # -------------------------------------------------

    error_handler = RotatingFileHandler(
        filename=ERROR_LOG_FILE,
        maxBytes=5 * 1024 * 1024,    # 5 MB
        backupCount=3,
        encoding="utf-8",
    )

    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # -------------------------------------------------
    # Register Handlers
    # -------------------------------------------------

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)

    root_logger.info("=" * 70)
    root_logger.info("Payment AI Platform Logging Initialized")
    root_logger.info("Log Level      : %s", LOG_LEVEL)
    root_logger.info("Application Log: %s", LOG_FILE)
    root_logger.info("Error Log      : %s", ERROR_LOG_FILE)
    root_logger.info("=" * 70)