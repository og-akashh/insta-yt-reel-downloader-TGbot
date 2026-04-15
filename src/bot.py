import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from .config import Config
from .handlers import start, handle_message, error_handler
from .utils import setup_logging, logger


# ... your other imports ...

def run_health_server():
    """Run a simple HTTP server for health checks (required by Render)"""
    # Read the port from the environment variable and ensure it's an integer
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    logger.info(f"Health check server running on port {port}")
    server.serve_forever()

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress health check logs
        pass

def run_health_server():
    """Run a simple HTTP server for health checks (required by Render)"""
    port = int(Config.PORT) if hasattr(Config, 'PORT') else 8000
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    logger.info(f"Health check server running on port {port}")
    server.serve_forever()

def main():
    Config.validate()
    logger = setup_logging(Config.LOG_LEVEL)
    
    # Start health check server in a separate thread (for Render)
    if Config.RENDER_DEPLOYMENT:
        health_thread = threading.Thread(target=run_health_server, daemon=True)
        health_thread.start()
        logger.info("Health check server started for Render deployment")
    
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
    
    # Start the bot with polling (works best on Render free tier)
    logger.info("Starting bot with long-polling...")
    application.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
