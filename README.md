# 🎥 Telegram Media Downloader Bot

A production-ready Telegram bot that downloads Instagram Reels and YouTube Shorts, then automatically deletes them after 20 minutes. Optimized for **Render.com** free tier deployment.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## ✨ Features

- ✅ Download Instagram Reels and YouTube Shorts
- ⏰ Auto-delete local files after 20 minutes
- 🗑️ Auto-delete sent messages from chat
- 🐳 Docker support for local development
- ⚡ Asynchronous & concurrent request handling
- 🚀 **One-click deploy to Render** (free tier)
- 📊 Automatic health checks and restart

## 🚀 Deploy to Render (Recommended)

### Option 1: One-Click Deploy (Easiest)

1. Click the "Deploy to Render" button above
2. Connect your GitHub repository
3. Add your `BOT_TOKEN` in environment variables
4. Click "Apply"
5. Your bot will be live in 2-3 minutes!

### Option 2: Manual Deploy

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service** on [Render](https://render.com)
   - Connect your GitHub repo
   - Name: `telegram-media-bot`
   - Environment: `Python 3`
   - Build Command:
     ```bash
     apt-get update && apt-get install -y ffmpeg
     pip install -r requirements.txt
