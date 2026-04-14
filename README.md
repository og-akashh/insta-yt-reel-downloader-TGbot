# 🎥 insta-yt-reel-downloader-TGbot

A production-ready Telegram bot that downloads Instagram Reels and YouTube Shorts, then automatically deletes them after 20 minutes.

## Features

- ✅ Download Instagram Reels and YouTube Shorts
- ⏰ Auto-delete local files after 20 minutes
- 🗑️ Auto-delete sent messages from chat
- 🐳 Docker support for easy deployment
- ⚡ Asynchronous & concurrent request handling
- 📊 Rate limiting and error handling

## Quick Start

1. **Get a Telegram Bot Token** from [@BotFather](https://t.me/botfather)
2. **Clone this repository**
3. **Copy `.env.example` to `.env`** and add your token
4. **Run** `./start.sh` (or `docker-compose up --build`)

## Deployment

### Railway (Free)
- Add `BOT_TOKEN` as environment variable
- Deploy from GitHub repository

### Heroku (Free Tier)
- Add `BOT_TOKEN` config var
- Deploy with `git push heroku main`

### VPS / Self-hosted
- Install Docker and Docker Compose
- Run `docker-compose up -d`

## Configuration

Edit `.env` to adjust:

| Variable               | Description                        |
| ---------------------- | ---------------------------------- |
| `BOT_TOKEN`            | Telegram bot token (required)     |
| `DELETE_AFTER_MINUTES` | Minutes until deletion (default 20)|
| `MAX_FILE_SIZE_MB`     | Max video size to send (default 50)|
| `LOG_LEVEL`            | `DEBUG`, `INFO`, `WARNING`, `ERROR`|

## License

MIT
