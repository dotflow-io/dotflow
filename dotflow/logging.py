"""Log"""

import logging

from dotflow.settings import Settings as settings

logger = logging.getLogger(settings.LOG_PROFILE)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter(settings.LOG_FORMAT))

logger.addHandler(ch)
