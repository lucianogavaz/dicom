from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DicomEndpoint
from app.db.session import get_db

router = APIRouter(prefix="/endpoints", tags=["endpoints"])


class EndpointCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    ae_title: str = Field(min_length=1, max_length=64)
    host: str = Field(min_length=1, max_length=255)
    port: int = Field(ge=1, le=65535)
    enabled: bool = True
    is_default: bool = False


@router.get("")
def list_endpoints(db: Session = Depends(get_db)) -> list[dict]:
    items = db.scalars(select(DicomEndpoint).order_by(DicomEndpoint.name.asc())).all()
    return [item.to_dict() for item in items]


@router.post("")
def create_endpoint(payload: EndpointCreate, db: Session = Depends(get_db)) -> dict:
    if payload.is_default:
        for endpoint in db.scalars(select(DicomEndpoint).where(DicomEndpoint.is_default.is_(True))).all():
            endpoint.is_default = False

    item = DicomEndpoint(
        name=payload.name,
        ae_title=payload.ae_title,
        host=payload.host,
        port=payload.port,
        enabled=payload.enabled,
        is_default=payload.is_default,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item.to_dict()


@router.post("/{endpoint_id}/test")
def test_endpoint(endpoint_id: UUID, db: Session = Depends(get_db)) -> dict:
    item = db.get(DicomEndpoint, endpoint_id)
    if not item:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return {
        "endpoint_id": str(item.id),
        "message": "Connectivity test stub created. Implement C-ECHO next.",
    }
