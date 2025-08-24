import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        os.path.join(log_dir, f"{name}.log"), maxBytes=1_000_000, backupCount=5
    )
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger