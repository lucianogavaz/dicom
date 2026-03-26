from datetime import datetime
from pathlib import Path

from app.core.config import settings


def save_incoming_dataset(ds, source_ae_title: str | None, source_ip: str | None) -> tuple[Path, dict]:
    study_uid = str(ds.StudyInstanceUID)
    series_uid = str(ds.SeriesInstanceUID)
    sop_uid = str(ds.SOPInstanceUID)
    day_path = datetime.utcnow().strftime("%Y/%m/%d")

    target_dir = settings.local_storage_path / day_path / study_uid / series_uid
    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / f"{sop_uid}.dcm"
    ds.save_as(file_path, enforce_file_format=True)

    metadata = {
        "study_instance_uid": study_uid,
        "series_instance_uid": series_uid,
        "sop_instance_uid": sop_uid,
        "sop_class_uid": str(ds.SOPClassUID),
        "transfer_syntax_uid": str(getattr(ds.file_meta, "TransferSyntaxUID", "")) or None,
        "modality": getattr(ds, "Modality", None),
        "patient_id": getattr(ds, "PatientID", None),
        "patient_name": str(getattr(ds, "PatientName", "")) or None,
        "source_ae_title": source_ae_title,
        "source_ip": source_ip,
        "file_path": str(file_path),
    }
    return file_path, metadata
