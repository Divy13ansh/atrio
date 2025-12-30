from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]  # atrio/

class Settings(BaseSettings):
    ENV: str = "dev"
    PROJECT_NAME: str = "Angio AI"
    DATABASE_URL: str

    DICOM_STORAGE_PATH: str = "storage/dicom"
    REPORT_STORAGE_PATH: str = "storage/reports"

    model_config = {
        "env_file": ".env",
        "extra": "allow",   # ✅ THIS FIXES IT
    }

settings = Settings()

