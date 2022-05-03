import os

LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s %(name)-16s %(levelname)-8s %(message)s"
API_KEY = os.environ.get("API_KEY")
API_KEY_NAME = "X-API-Key"