"""Log"""

import logging
import logging.config

from dotflow.settings import Settings as settings

settings.START_PATH.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=settings.LOG_PATH,
    format=settings.LOG_FORMAT,
    level=logging.INFO,
    filemode="a",
)

logger = logging.getLogger(settings.LOG_PROFILE)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    settings.LOG_FORMAT
)

ch.setFormatter(formatter)

logger.addHandler(ch)
