"""Log"""

import logging
import logging.config

from dotflow.core.utils import make_dir
from dotflow.settings import Settings as settings

make_dir(path=settings.INITIAL_PATH, show_log=True)

logging.basicConfig(
    filename=settings.LOG_PATH,
    level=logging.INFO,
    filemode="a"
)

logger = logging.getLogger(settings.LOG_PROFILE)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s [%(name)s]: %(message)s'
)

ch.setFormatter(formatter)

logger.addHandler(ch)
