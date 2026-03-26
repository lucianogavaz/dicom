import logging
from pathlib import Path

from app.core.config import settings


def configure_logging() -> None:
    settings.log_path.mkdir(parents=True, exist_ok=True)
    log_file = Path(settings.log_path) / "app.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

