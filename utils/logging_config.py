from logging.config import dictConfig
import os
from pathlib import Path

from dotenv import load_dotenv

from modules.variables.definitions import ROOT


def get_path_to_logs() -> Path:
    """
    Determines the appropriate filesystem location for log files by checking environment configuration, creating the log directory if it does not exist, and providing the resulting log file path

        Returns:
            Path object that contains the path to the log file

    """

    load_dotenv(Path(ROOT, "config.env"))

    log_folder = "/var/log/biam_urb"

    if os.environ.get("PATH_TO_LOGS", "") == "":
        app_log_folder = Path(log_folder)
    else:
        app_log_folder = os.environ.get("PATH_TO_LOGS")

    try:
        os.mkdir(Path(app_log_folder))
    except FileExistsError:
        pass

    return Path(app_log_folder, "main.log")


PATH_TO_LOGS = get_path_to_logs()
CORR_ID_LENGTH = 16


def configure_logging() -> None:
    """
    Sets up a comprehensive logging system by defining handlers, filters, and formatters to ensure clear and context-rich log output. Enables customization of loggers, integrates correlation IDs for traceability, and utilizes file rotation to manage log storage efficiently.

        Logger configuration examples:
        'databases': {
            'handlers': ['console'],
            'level': 'WARNING'
        }
        'httpx': {
            'handlers': ['console'],
            'level': 'INFO'
        }

        For more details:
        https://docs.python.org/3/library/logging.config.html#configuration-
        dictionary-schema
        https://stackoverflow.com/questions/7507825/where-is-a-complete-example-of-
        logging-config-dictconfig

        If you need to use a logger in your module just create one with
        logging.getLogger(__name__). This will create a logger with the full module
        name and 'root' logger settings.

        The length of ID for logging to which CorrelationID will be trimmed can
        be specified using the CORR_ID_LENGTH constant.

        The RotatingFileHandler with the following parameters is used for logging:
        - max file size is 10.5 MB
        - number of backups is 5 (i.e. 5 files with log history will be stored
        simultaneously, which will overwrite each other one by one from 1 to 5 when
        the max size is reached)

    """

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": CORR_ID_LENGTH,
                    "default_value": "-",
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(levelname)s: %(asctime)s "
                    "%(name)s:%(lineno)d "
                    "[%(correlation_id)s] %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filters": ["correlation_id"],
                    "formatter": "console",
                    "filename": PATH_TO_LOGS,
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 5,
                },
            },
            "loggers": {
                # project logger (root)
                "": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )
