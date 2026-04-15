from telegram import Update
from telegram.ext import ContextTypes, JobQueue
from .downloader import VideoDownloader
from .utils import (
    is_supported_url,
    delete_file_async,
    logger,
)
from .config import Config
import os

downloader = VideoDownloader()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎥 Send me an Instagram Reel or YouTube Shorts link, and I'll download it for you!\n\n"
        "Supported links:\n"
        "• Instagram Reel: https://instagram.com/reel/...\n"
        "• YouTube Shorts: https://youtube.com/shorts/...\n\n"
        "Videos are automatically deleted after 20 minutes."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.effective_chat.id

    if not is_supported_url(url):
        await update.message.reply_text("❌ Unsupported link. Please send an Instagram Reel or YouTube Shorts URL.")
        return

    status_msg = await update.message.reply_text("⏳ Downloading... Please wait.")

    # Download the video
    file_path, title = await downloader.download(url)
    if not file_path:
        await status_msg.edit_text(f"❌ Download failed: {title}")
        return

    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > Config.MAX_FILE_SIZE_MB:
        await status_msg.edit_text(f"❌ File too large ({file_size_mb:.1f} MB). Max: {Config.MAX_FILE_SIZE_MB} MB")
        os.remove(file_path)
        return

    # Send video to user
    try:
        with open(file_path, "rb") as video:
            await context.bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=f"✅ Downloaded: {title}\n\n⏰ This video will be deleted from chat in {Config.DELETE_AFTER_MINUTES} minutes.",
                supports_streaming=True,
            )
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ Failed to send video: {e}")
        os.remove(file_path)
        return

    # Schedule local file deletion after 20 minutes
    asyncio.create_task(delete_file_async(file_path, Config.DELETE_AFTER_MINUTES * 60))

    # Schedule chat message deletion (requires job queue)
    if context.job_queue:
        context.job_queue.run_once(
            delete_chat_message,
            Config.DELETE_AFTER_MINUTES * 60,
            data={"chat_id": chat_id, "message_id": update.message.message_id + 1}  # approx the sent video
        )

async def delete_chat_message(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    try:
        await context.bot.delete_message(chat_id=data["chat_id"], message_id=data["message_id"])
        logger.info(f"Deleted chat message {data['message_id']} in {data['chat_id']}")
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ An error occurred. Please try again later."
        )
