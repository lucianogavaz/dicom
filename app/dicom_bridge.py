from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import Dict, List

from pydicom.dataset import Dataset
from pynetdicom import AE, evt
from pynetdicom.sop_class import Verification
from pynetdicom import StoragePresentationContexts, AllStoragePresentationContexts

logger = logging.getLogger(__name__)


@dataclass
class BridgeConfig:
    listen_ae_title: str
    listen_port: int
    pacs_ae_title: str
    pacs_host: str
    pacs_port: int


class DicomBridge:
    """
    Ponte DICOM:
    - SCP (servidor) para receber C-STORE
    - SCU (cliente) para retransmitir para um PACS DICOM Store
    """

    def __init__(self, config: BridgeConfig):
        self.config = config
        self._server = None
        self._lock = threading.Lock()
        self._stats: Dict[str, int] = {
            "received": 0,
            "forwarded": 0,
            "failed_forward": 0,
        }
        self._last_errors: List[str] = []

    def start(self) -> None:
        handlers = [(evt.EVT_C_STORE, self._on_c_store), (evt.EVT_C_ECHO, self._on_c_echo)]

        ae = AE(ae_title=self.config.listen_ae_title)
        for cx in StoragePresentationContexts:
            ae.add_supported_context(cx.abstract_syntax)
        ae.add_supported_context(Verification)

        self._server = ae.start_server(
            ("0.0.0.0", self.config.listen_port),
            evt_handlers=handlers,
            block=False,
        )
        logger.info(
            "DICOM SCP online em %s:%s AE=%s",
            "0.0.0.0",
            self.config.listen_port,
            self.config.listen_ae_title,
        )

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            logger.info("DICOM SCP finalizado")

    def _on_c_echo(self, _event):
        return 0x0000

    def _on_c_store(self, event):
        ds = event.dataset
        ds.file_meta = event.file_meta

        with self._lock:
            self._stats["received"] += 1

        sop_instance_uid = getattr(ds, "SOPInstanceUID", "desconhecido")
        logger.info("Recebido SOPInstanceUID=%s, iniciando encaminhamento", sop_instance_uid)

        success = self._forward_to_pacs(ds)
        with self._lock:
            if success:
                self._stats["forwarded"] += 1
            else:
                self._stats["failed_forward"] += 1

        # status de sucesso do armazenamento local do SCP
        return 0x0000

    def _forward_to_pacs(self, ds: Dataset) -> bool:
        scu = AE(ae_title=f"{self.config.listen_ae_title[:12]}_FWD")
        for cx in AllStoragePresentationContexts:
            scu.add_requested_context(cx.abstract_syntax)

        assoc = scu.associate(
            self.config.pacs_host,
            self.config.pacs_port,
            ae_title=self.config.pacs_ae_title,
        )
        if not assoc.is_established:
            message = (
                f"Falha ao associar com PACS {self.config.pacs_host}:{self.config.pacs_port} "
                f"AE={self.config.pacs_ae_title}"
            )
            self._remember_error(message)
            logger.error(message)
            return False

        status = assoc.send_c_store(ds)
        assoc.release()

        if not status or status.Status != 0x0000:
            code = getattr(status, "Status", None)
            message = f"C-STORE para PACS retornou status inválido: {code}"
            self._remember_error(message)
            logger.error(message)
            return False

        logger.info(
            "Encaminhado com sucesso para PACS %s:%s", self.config.pacs_host, self.config.pacs_port
        )
        return True

    def _remember_error(self, message: str) -> None:
        with self._lock:
            self._last_errors.insert(0, message)
            self._last_errors = self._last_errors[:20]

    def snapshot(self) -> Dict[str, object]:
        with self._lock:
            return {
                "config": {
                    "listen_ae_title": self.config.listen_ae_title,
                    "listen_port": self.config.listen_port,
                    "pacs_ae_title": self.config.pacs_ae_title,
                    "pacs_host": self.config.pacs_host,
                    "pacs_port": self.config.pacs_port,
                },
                "stats": dict(self._stats),
                "last_errors": list(self._last_errors),
            }
