import logging
from example.config import LOGGER_LEVEL, LOG_FORMAT

logging.basicConfig(
    format=LOG_FORMAT, level=LOGGER_LEVEL
)
logging.getLogger('uvicorn').setLevel(LOGGER_LEVEL)

from example.app import app
