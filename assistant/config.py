"""Local Assistant configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
MEMORY_DB_PATH = DATA_DIR / "memory.db"

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_IDS = {int(uid) for uid in os.getenv("ALLOWED_USER_IDS", "").split(",") if uid.strip()}

# SearxNG
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:4000")

# Document watching
WATCHED_DIRS = [
    d.strip()
    for d in os.getenv("WATCHED_DIRS", "").split(",")
    if d.strip()
]
WATCHED_EXTENSIONS = {".pdf", ".md", ".txt", ".docx", ".html"}

# Agent
MAX_AGENT_ITERATIONS = 5
CONTEXT_WINDOW_MESSAGES = 20
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# FastAPI
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8100"))
