import logging
import time
from datetime import datetime

from sqlalchemy import select

from app.core.config import settings
from app.db.models import DicomInstanceQueue
from app.db.session import SessionLocal
from app.services.dicom_sender import send_to_default_pacs

LOGGER = logging.getLogger(__name__)


def process_pending_items() -> None:
    with SessionLocal() as db:
        stmt = (
            select(DicomInstanceQueue)
            .where(DicomInstanceQueue.status.in_(("PENDING_SEND", "RETRY_PENDING")))
            .order_by(DicomInstanceQueue.received_at.asc())
            .limit(10)
        )
        items = db.scalars(stmt).all()

        for item in items:
            item.status = "SENDING"
            item.last_attempt_at = datetime.utcnow()
            db.commit()

            try:
                status = send_to_default_pacs(item.file_path)
                if status == 0x0000:
                    item.status = "SENT"
                    item.sent_at = datetime.utcnow()
                    item.last_error = None
                else:
                    item.retry_count += 1
                    item.status = "FAILED" if item.retry_count >= item.max_retries else "RETRY_PENDING"
                    item.last_error = f"C-STORE status {hex(status)}"
            except Exception as exc:
                item.retry_count += 1
                item.status = "FAILED" if item.retry_count >= item.max_retries else "RETRY_PENDING"
                item.last_error = str(exc)
                LOGGER.exception("Failed sending queue item %s", item.id)

            db.commit()


def run_worker() -> None:
    LOGGER.info("Starting sender worker with poll interval %s seconds", settings.worker_poll_seconds)
    while True:
        process_pending_items()
        time.sleep(settings.worker_poll_seconds)

