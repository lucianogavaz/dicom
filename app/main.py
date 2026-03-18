from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.dicom_bridge import BridgeConfig, DicomBridge

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")

bridge = DicomBridge(
    BridgeConfig(
        listen_ae_title=os.getenv("DICOM_LISTEN_AE_TITLE", "DICOMRCV"),
        listen_port=int(os.getenv("DICOM_LISTEN_PORT", "11112")),
        pacs_ae_title=os.getenv("PACS_AE_TITLE", "DICOMSTORE"),
        pacs_host=os.getenv("PACS_HOST", "127.0.0.1"),
        pacs_port=int(os.getenv("PACS_PORT", "104")),
    )
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    bridge.start()
    yield
    bridge.stop()


app = FastAPI(
    title="DICOM Receiver + Forwarder",
    description="Recebe DICOM via C-STORE e encaminha para um PACS DICOM Store.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/status")
def status():
    return bridge.snapshot()
