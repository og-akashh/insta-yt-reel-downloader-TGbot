import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from .config import Config
from .handlers import start, handle_message, error_handler
from .utils import setup_logging

def main():
    Config.validate()
    logger = setup_logging(Config.LOG_LEVEL)

    # Build the application
    application = (
        Application.builder()
        .token(Config.BOT_TOKEN)
        .concurrent_updates(True)
        .build()
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Start the bot
    if Config.USE_WEBHOOK:
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.WEBHOOK_PORT,
            url_path=Config.BOT_TOKEN,
            webhook_url=f"{Config.WEBHOOK_URL}/{Config.BOT_TOKEN}",
        )
    else:
        application.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
