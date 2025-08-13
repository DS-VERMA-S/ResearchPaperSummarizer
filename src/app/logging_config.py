import logging
import os
from typing import Optional


def setup_logging(level: Optional[str] = None) -> None:
    """Configure application and uvicorn loggers with a consistent format.

    The function is idempotent and safe to call multiple times.
    """
    resolved_level_name = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    resolved_level = getattr(logging, resolved_level_name, logging.INFO)

    root_logger = logging.getLogger()
    if root_logger.handlers:
        # Already configured; update level only
        root_logger.setLevel(resolved_level)
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(resolved_level)
    stream_handler.setFormatter(formatter)

    root_logger.setLevel(resolved_level)
    root_logger.addHandler(stream_handler)

    # Align uvicorn loggers
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True
        logger.setLevel(resolved_level)


def get_logger(name: str) -> logging.Logger:
    """Convenience helper to get a namespaced logger."""
    return logging.getLogger(name)