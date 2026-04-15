import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Deployment settings
    RENDER_DEPLOYMENT = os.getenv("RENDER_DEPLOYMENT", "false").lower() == "true"
    PORT = int(os.getenv("PORT", 8000)) # Render sets this automatically
    
    # Download settings
    DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "downloads")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 50))
    MAX_VIDEO_DURATION = int(os.getenv("MAX_VIDEO_DURATION", 120))
    DELETE_AFTER_MINUTES = int(os.getenv("DELETE_AFTER_MINUTES", 20))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")
        
        # Create download directory
        os.makedirs(cls.DOWNLOAD_PATH, exist_ok=True)
