"""Local Assistant configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_IDS = {int(uid) for uid in os.getenv("ALLOWED_USER_IDS", "").split(",") if uid.strip()}

# Obsidian vault (ruya, gunluk, spor notlari)
OBSIDIAN_VAULT = os.getenv("OBSIDIAN_VAULT", "~/ObsidianVault")
