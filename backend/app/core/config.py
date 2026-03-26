from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "dicom-gateway"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "sqlite:///./dicom_gateway.db"

    local_ae_title: str = "XA_RECEIVER"
    local_dicom_port: int = 11112
    local_storage_path: Path = Field(default=Path("C:/dicom_gateway/storage/incoming"))

    default_remote_ae_title: str = "PACS_AE"
    default_remote_host: str = "127.0.0.1"
    default_remote_port: int = 104

    worker_poll_seconds: int = 10
    max_retries: int = 5
    log_path: Path = Field(default=Path("C:/dicom_gateway/logs"))


settings = Settings()

