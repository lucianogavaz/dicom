from pydicom import dcmread
from pynetdicom import AE
from pynetdicom.sop_class import EnhancedXAImageStorage, Verification, XRayAngiographicImageStorage

from app.core.config import settings


def send_to_default_pacs(file_path: str) -> int:
    ds = dcmread(file_path)
    ae = AE(ae_title=settings.local_ae_title)
    ae.add_requested_context(XRayAngiographicImageStorage)
    ae.add_requested_context(EnhancedXAImageStorage)
    ae.add_requested_context(Verification)

    transfer_syntax = getattr(ds.file_meta, "TransferSyntaxUID", None)
    if transfer_syntax:
        ae.add_requested_context(ds.SOPClassUID, [transfer_syntax])

    assoc = ae.associate(
        settings.default_remote_host,
        settings.default_remote_port,
        ae_title=settings.default_remote_ae_title,
    )
    if not assoc.is_established:
        raise RuntimeError("Failed to associate with PACS")

    status = assoc.send_c_store(ds)
    assoc.release()

    if not status:
        raise RuntimeError("C-STORE returned no status")

    return int(status.Status)
