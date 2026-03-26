from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import DicomInstanceQueue
from app.db.session import get_db

router = APIRouter(prefix="/queue", tags=["resend"])


@router.post("/{item_id}/resend")
def resend_queue_item(item_id: UUID, db: Session = Depends(get_db)) -> dict:
    item = db.get(DicomInstanceQueue, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")

    item.status = "RETRY_PENDING"
    item.last_error = None
    db.commit()
    db.refresh(item)
    return item.to_dict()

