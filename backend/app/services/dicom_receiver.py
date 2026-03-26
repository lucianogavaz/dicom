import logging

from pydicom.dataset import FileMetaDataset
from pynetdicom import AE, evt
from pynetdicom.presentation import StoragePresentationContexts
from pynetdicom.sop_class import Verification

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.dicom_validator import validate_dataset
from app.services.file_store import save_incoming_dataset
from app.services.queue_service import create_queue_item

LOGGER = logging.getLogger(__name__)


def handle_echo(_event):
    return 0x0000


def handle_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta or FileMetaDataset()

    ok, error = validate_dataset(ds)
    if not ok:
        LOGGER.warning("Rejected incoming object: %s", error)
        return 0xC210

    source_ae = getattr(event.assoc.requestor, "ae_title", "")
    source_ip = getattr(event.assoc.requestor, "address", "")
    _, metadata = save_incoming_dataset(ds, str(source_ae).strip(), str(source_ip).strip())

    with SessionLocal() as db:
        item = create_queue_item(db, metadata)
        LOGGER.info(
            "Queued instance %s with id %s for patient %s",
            metadata["sop_instance_uid"],
            item.id,
            metadata.get("patient_name") or metadata.get("patient_id") or "unknown",
        )

    return 0x0000


def start_receiver() -> None:
    ae = AE(ae_title=settings.local_ae_title)
    for context in StoragePresentationContexts:
        ae.add_supported_context(context.abstract_syntax, context.transfer_syntax)
    ae.add_supported_context(Verification)

    handlers = [
        (evt.EVT_C_ECHO, handle_echo),
        (evt.EVT_C_STORE, handle_store),
    ]
    LOGGER.info("Starting DICOM receiver on port %s", settings.local_dicom_port)
    ae.start_server(("0.0.0.0", settings.local_dicom_port), block=True, evt_handlers=handlers)
