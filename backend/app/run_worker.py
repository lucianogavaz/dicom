from app.core.logging import configure_logging
from app.db.base import Base
from app.db.session import engine
from app.workers.sender_worker import run_worker

configure_logging()
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    run_worker()

