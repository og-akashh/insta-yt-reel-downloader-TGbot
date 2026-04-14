#!/bin/bash
set -e

if [ ! -f .env ]; then
    echo "Creating .env from .env.example"
    cp .env.example .env
    echo "Please edit .env and add your BOT_TOKEN"
    exit 1
fi

docker-compose up --build
