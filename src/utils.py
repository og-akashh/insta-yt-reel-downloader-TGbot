import logging
import re
import os
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def setup_logging(level):
    logger.setLevel(level)
    return logger

def is_instagram_reel(url: str) -> bool:
    pattern = r"(https?://)?(www\.)?(instagram\.com|instagr\.am)/reel/[a-zA-Z0-9_-]+"
    return bool(re.match(pattern, url))

def is_youtube_short(url: str) -> bool:
    patterns = [
        r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/shorts/[a-zA-Z0-9_-]+",
        r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/watch\?v=[a-zA-Z0-9_-]+&?.*",
    ]
    return any(re.match(p, url) for p in patterns)

def is_supported_url(url: str) -> bool:
    return is_instagram_reel(url) or is_youtube_short(url)

async def delete_file_async(file_path: str, delay_seconds: int = 0):
    """Delete a file after a delay asynchronously."""
    await asyncio.sleep(delay_seconds)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete {file_path}: {e}")

def safe_filename(title: str, ext: str = "mp4") -> str:
    """Generate a safe filename from title."""
    safe = re.sub(r'[\\/*?:"<>|]', "", title)
    safe = safe.strip().replace(" ", "_")[:50]
    return f"{safe}.{ext}"
