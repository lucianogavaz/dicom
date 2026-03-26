SUPPORTED_SOP_CLASSES = {
    "1.2.840.10008.5.1.4.1.1.12.1",  # XA Image Storage
    "1.2.840.10008.5.1.4.1.1.12.1.1",  # Enhanced XA Image Storage
}

REQUIRED_FIELDS = (
    "StudyInstanceUID",
    "SeriesInstanceUID",
    "SOPInstanceUID",
    "SOPClassUID",
)


def validate_dataset(ds) -> tuple[bool, str | None]:
    for field in REQUIRED_FIELDS:
        if not getattr(ds, field, None):
            return False, f"Missing required field: {field}"

    if str(ds.SOPClassUID) not in SUPPORTED_SOP_CLASSES:
        return False, f"Unsupported SOP Class: {ds.SOPClassUID}"

    return True, None

