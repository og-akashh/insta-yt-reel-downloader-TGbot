FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create downloads directory
RUN mkdir -p /app/downloads

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "-m", "src.bot"]
