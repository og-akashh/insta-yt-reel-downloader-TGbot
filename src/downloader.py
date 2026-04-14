import yt_dlp
import asyncio
import os
from .config import Config
from .utils import logger, safe_filename

class VideoDownloader:
    def __init__(self):
        self.download_path = Config.DOWNLOAD_PATH
        os.makedirs(self.download_path, exist_ok=True)

    def _get_ydl_opts(self, output_template: str):
        return {
            "outtmpl": output_template,
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            "ignoreerrors": True,
            "retries": 3,
            "fragment_retries": 3,
            "ratelimit": 10000000,  # 10 MB/s rate limit
        }

    async def download(self, url: str) -> tuple[str, str] | tuple[None, str]:
        """
        Download video from URL.
        Returns: (file_path, title) or (None, error_message)
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._sync_download, url)

    def _sync_download(self, url: str):
        try:
            with yt_dlp.YoutubeDL(self._get_ydl_opts(f"{self.download_path}/%(title)s.%(ext)s")) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                if not os.path.exists(file_path):
                    # Fallback for merged files
                    file_path = file_path.rsplit(".", 1)[0] + ".mp4"
                title = info.get("title", "video")
                logger.info(f"Downloaded: {title}")
                return file_path, title
        except Exception as e:
            logger.error(f"Download failed for {url}: {e}")
            return None, str(e)
