import logging
import logging.config
import os
from typing import Any, Dict

def get_logging_config(level: str | None = None) -> Dict[str, Any]:
    log_level = (level or os.getenv("LOG_LEVEL") or "INFO").upper()
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": log_level,
            },
            "luna": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "luna.middleware": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "luna.llm": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
        },
    }

def setup_logging(level: str | None = None) -> None:
    cfg = get_logging_config(level)
    logging.config.dictConfig(cfg)
    logging.getLogger("luna").info("🌙 Luna logging configured with level=%s", level or os.getenv("LOG_LEVEL") or "INFO")
