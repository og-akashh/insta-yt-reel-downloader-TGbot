FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (ffmpeg is required for video processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists

# Copy only requirements first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create the downloads directory (mounted as a volume in production)
RUN mkdir -p /app/downloads

# Set environment variable to disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "-m", "src.bot"]
