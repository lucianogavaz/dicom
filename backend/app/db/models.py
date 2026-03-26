from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DicomEndpoint(Base):
    __tablename__ = "dicom_endpoints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    ae_title: Mapped[str] = mapped_column(String(64), nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "ae_title": self.ae_title,
            "host": self.host,
            "port": self.port,
            "enabled": self.enabled,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat(),
        }


class DicomInstanceQueue(Base):
    __tablename__ = "dicom_instance_queue"
    __table_args__ = (UniqueConstraint("sop_instance_uid", "destination_ae_title", name="uq_instance_destination"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    study_instance_uid: Mapped[str] = mapped_column(String(128), nullable=False)
    series_instance_uid: Mapped[str] = mapped_column(String(128), nullable=False)
    sop_instance_uid: Mapped[str] = mapped_column(String(128), nullable=False)
    sop_class_uid: Mapped[str] = mapped_column(String(128), nullable=False)
    transfer_syntax_uid: Mapped[str | None] = mapped_column(String(128))
    modality: Mapped[str | None] = mapped_column(String(16))
    patient_id: Mapped[str | None] = mapped_column(String(64))
    patient_name: Mapped[str | None] = mapped_column(String(255))
    source_ae_title: Mapped[str | None] = mapped_column(String(64))
    source_ip: Mapped[str | None] = mapped_column(String(64))
    destination_endpoint_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("dicom_endpoints.id"))
    destination_ae_title: Mapped[str | None] = mapped_column(String(64))
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="PENDING_SEND", nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    last_error: Mapped[str | None] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "study_instance_uid": self.study_instance_uid,
            "series_instance_uid": self.series_instance_uid,
            "sop_instance_uid": self.sop_instance_uid,
            "sop_class_uid": self.sop_class_uid,
            "transfer_syntax_uid": self.transfer_syntax_uid,
            "modality": self.modality,
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "source_ae_title": self.source_ae_title,
            "source_ip": self.source_ip,
            "destination_endpoint_id": self.destination_endpoint_id,
            "destination_ae_title": self.destination_ae_title,
            "file_path": self.file_path,
            "status": self.status,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "last_error": self.last_error,
            "received_at": self.received_at.isoformat(),
            "last_attempt_at": self.last_attempt_at.isoformat() if self.last_attempt_at else None,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
        }
