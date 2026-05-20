import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("wealth_advisor")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    filename=f"{LOG_DIR}/wealth_advisor.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)