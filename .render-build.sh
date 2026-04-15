#!/bin/bash
set -e  # exit on any error

echo "Installing system dependencies..."
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg
apt-get clean

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully."
