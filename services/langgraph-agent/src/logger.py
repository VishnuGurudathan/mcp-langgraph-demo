import logging
from .config.settings import settings

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL.upper())
    if not logger.handlers:
        h = logging.StreamHandler()
        fmt = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
        h.setFormatter(fmt)
        logger.addHandler(h)
    return logger
