import os

from datetime import date
import logging
from logging.config import dictConfig

from config.const import PROJECT_NAME

parent_path_index = os.getcwd().find(PROJECT_NAME)
LOG_DIR = os.path.join(os.getcwd()[:parent_path_index], PROJECT_NAME, "logs")

LOG_LEVEL: str = "DEBUG"
FORMAT: str = (
    "%(levelprefix)s %(asctime)s | %(module)s.%(filename)s: %(lineno)d |" " %(message)s"
)
FORMAT_FILE: str = (
    " %(levelname)-8s [%(asctime)s][%(module)s.%(filename)s"
    " %(lineno)d]  %(message)s "
)

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": FORMAT,
        },
        "filr": {
            "format": FORMAT_FILE,
        },
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "filr",
            "filename": (f"{LOG_DIR}/{date.today().strftime('%Y-%m-%d')}.log"),
            # "filename": (f"logs/{date.today().strftime('%Y-%m-%d')}.log"),
            "encoding": "utf-8",
            "level": LOG_LEVEL,
        },
    },
    "loggers": {
        "__name__": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
        }
    },
}


def set_logger():
    dictConfig(logging_config)

    return logging.getLogger("__name__")
