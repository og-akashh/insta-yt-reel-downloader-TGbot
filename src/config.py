import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    USE_WEBHOOK = os.getenv("USE_WEBHOOK", "False").lower() == "true"
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 8443))

    DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 50))
    MAX_VIDEO_DURATION = int(os.getenv("MAX_VIDEO_DURATION", 120))
    DELETE_AFTER_MINUTES = int(os.getenv("DELETE_AFTER_MINUTES", 20))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")
