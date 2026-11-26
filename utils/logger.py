"""Activity logging to outputs/logs/activity.log."""
import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "outputs" / "logs" / "activity.log"


def get_logger(name="os_sim"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
