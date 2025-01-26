import os
import logging
import coloredlogs

from config.settings import settings
from utils.log_formatter import ColoredFormatter

logger = logging.getLogger(__name__)

def get_log_level():
    loglev = settings.LOG_LEVEL
    return logging.DEBUG if loglev == "DEBUG" else \
        logging.INFO if loglev == "INFO" else \
        logging.WARN if loglev == "WARN" else \
        logging.ERROR if loglev == "ERROR" else logging.CRITICAL


def setup_logging():

    # logger.setLevel(get_log_level())
    #
    # handler = logging.StreamHandler()
    # handler.setFormatter(ColoredFormatter())
    #
    # logger.addHandler(handler)

    coloredlogs.install(level='DEBUG')

    logging.basicConfig(
        level=get_log_level(),
        format="%(asctime)s : %(levelname)s : %(message)s"
    )


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
