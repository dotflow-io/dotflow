import logging
import logging.config

from dotflow.config import Config as initial_config

config = initial_config()

logging.basicConfig(
    filename=config.logger_path,
    level=logging.INFO,
    filemode="a"
)

logger = logging.getLogger(config.logger_name)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s [%(name)s]: %(message)s'
)

ch.setFormatter(formatter)

logger.addHandler(ch)
