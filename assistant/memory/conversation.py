"""Conversation history manager backed by SQLite."""

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict

from assistant.config import MEMORY_DB_PATH, CONTEXT_WINDOW_MESSAGES

logger = logging.getLogger(__name__)


class ConversationMemory:
    """Stores and retrieves conversation history per user."""

    def __init__(self, db_path: Path = MEMORY_DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        schema_path = Path(__file__).parent.parent / "db" / "schema.sql"
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema_path.read_text())

    def add_message(self, user_id: int, role: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
                (user_id, role, content),
            )

    def get_history(self, user_id: int, limit: int = CONTEXT_WINDOW_MESSAGES) -> List[Dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT role, content FROM conversations WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        # Reverse so oldest first
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def clear_history(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))

    def get_recent_text(self, user_id: int, limit: int = 10) -> str:
        """Get recent messages as plain text (for fact extraction)."""
        history = self.get_history(user_id, limit)
        lines = []
        for msg in history:
            prefix = "Kullanici" if msg["role"] == "user" else "Asistan"
            lines.append(f"{prefix}: {msg['content']}")
        return "\n".join(lines)
