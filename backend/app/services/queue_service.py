from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import DicomEndpoint, DicomInstanceQueue


def get_default_endpoint(db: Session) -> DicomEndpoint | None:
    return db.scalar(
        select(DicomEndpoint).where(DicomEndpoint.enabled.is_(True), DicomEndpoint.is_default.is_(True))
    )


def create_queue_item(db: Session, metadata: dict) -> DicomInstanceQueue:
    endpoint = get_default_endpoint(db)
    destination_ae_title = endpoint.ae_title if endpoint else settings.default_remote_ae_title

    existing_item = db.scalar(
        select(DicomInstanceQueue).where(
            DicomInstanceQueue.sop_instance_uid == metadata["sop_instance_uid"],
            DicomInstanceQueue.destination_ae_title == destination_ae_title,
        )
    )
    if existing_item:
        existing_item.file_path = metadata["file_path"]
        existing_item.transfer_syntax_uid = metadata.get("transfer_syntax_uid")
        existing_item.modality = metadata.get("modality")
        existing_item.patient_id = metadata.get("patient_id")
        existing_item.patient_name = metadata.get("patient_name")
        existing_item.source_ae_title = metadata.get("source_ae_title")
        existing_item.source_ip = metadata.get("source_ip")
        if existing_item.status != "SENT":
            existing_item.status = "RETRY_PENDING"
            existing_item.last_error = None
        db.commit()
        db.refresh(existing_item)
        return existing_item

    item = DicomInstanceQueue(
        study_instance_uid=metadata["study_instance_uid"],
        series_instance_uid=metadata["series_instance_uid"],
        sop_instance_uid=metadata["sop_instance_uid"],
        sop_class_uid=metadata["sop_class_uid"],
        transfer_syntax_uid=metadata.get("transfer_syntax_uid"),
        modality=metadata.get("modality"),
        patient_id=metadata.get("patient_id"),
        patient_name=metadata.get("patient_name"),
        source_ae_title=metadata.get("source_ae_title"),
        source_ip=metadata.get("source_ip"),
        destination_endpoint_id=endpoint.id if endpoint else None,
        destination_ae_title=destination_ae_title,
        file_path=metadata["file_path"],
        status="PENDING_SEND",
        max_retries=settings.max_retries,
    )
    db.add(item)
    try:
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        return db.scalar(
            select(DicomInstanceQueue).where(
                DicomInstanceQueue.sop_instance_uid == metadata["sop_instance_uid"],
                DicomInstanceQueue.destination_ae_title == destination_ae_title,
            )
        )
