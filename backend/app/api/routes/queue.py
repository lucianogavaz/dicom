from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DicomInstanceQueue
from app.db.session import get_db

router = APIRouter(prefix="/queue", tags=["queue"])


@router.get("")
def list_queue(
    status: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[dict]:
    stmt = select(DicomInstanceQueue).order_by(DicomInstanceQueue.received_at.desc()).limit(limit)
    if status:
        stmt = stmt.where(DicomInstanceQueue.status == status)
    items = db.scalars(stmt).all()
    return [item.to_dict() for item in items]


@router.get("/{item_id}")
def get_queue_item(item_id: UUID, db: Session = Depends(get_db)) -> dict:
    item = db.get(DicomInstanceQueue, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    return item.to_dict()

