from fastapi import FastAPI

from app.api.routes.endpoints import router as endpoints_router
from app.api.routes.health import router as health_router
from app.api.routes.queue import router as queue_router
from app.api.routes.resend import router as resend_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import engine

configure_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(queue_router)
app.include_router(endpoints_router)
app.include_router(resend_router)

