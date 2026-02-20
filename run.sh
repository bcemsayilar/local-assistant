#!/bin/bash
# Local Assistant - Startup Script

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Check Ollama
if ! command -v ollama &>/dev/null; then
    echo "Ollama kurulu degil! https://ollama.com"
    exit 1
fi

# Check Ollama server
if ! curl -s http://localhost:11434/api/version &>/dev/null; then
    echo "Ollama server baslatiliyor..."
    ollama serve &
    sleep 2
fi

# Check required models
echo "Modeller kontrol ediliyor..."
ollama list | grep -q "qwen3:4b" || {
    echo "qwen3:4b indiriliyor..."
    ollama pull qwen3:4b
}

ollama list | grep -q "nomic-embed-text" || {
    echo "nomic-embed-text indiriliyor..."
    ollama pull nomic-embed-text
}

# Virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment olusturuluyor..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
pip install -q -r requirements.txt

# Check .env
if [ ! -f ".env" ]; then
    echo ".env dosyasi bulunamadi! .env.example'i kopyalayin:"
    echo "  cp .env.example .env"
    echo "  # TELEGRAM_BOT_TOKEN'i doldurun"
    exit 1
fi

# Run
echo "Local Assistant baslatiliyor..."
python -m assistant.main
