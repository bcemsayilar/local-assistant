"""Long-term fact extraction and storage."""

import sqlite3
import logging
from pathlib import Path
from typing import List

import ollama

from assistant.config import MEMORY_DB_PATH, OLLAMA_MODEL, OLLAMA_BASE_URL
from assistant.agent.prompts import FACT_EXTRACTION_PROMPT

logger = logging.getLogger(__name__)


class FactMemory:
    """Extracts and stores long-term facts about users."""

    def __init__(self, db_path: Path = MEMORY_DB_PATH):
        self.db_path = db_path
        self.client = ollama.Client(host=OLLAMA_BASE_URL, timeout=120)

    def extract_facts(self, conversation_text: str) -> List[str]:
        """Use LLM to extract memorable facts from conversation."""
        try:
            prompt = FACT_EXTRACTION_PROMPT.format(conversation=conversation_text)
            response = self.client.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1, "num_ctx": 2048},
            )
            text = response.get("message", {}).get("content", "").strip()
            if not text or text.upper() == "YOK":
                return []
            return [line.strip("- ").strip() for line in text.split("\n") if line.strip() and line.strip() != "YOK"]
        except Exception as e:
            logger.error(f"Fact extraction error: {e}")
            return []

    def save_facts(self, user_id: int, facts: List[str]):
        if not facts:
            return
        with sqlite3.connect(self.db_path) as conn:
            for fact in facts:
                # Avoid duplicates
                existing = conn.execute(
                    "SELECT id FROM facts WHERE user_id = ? AND fact = ?",
                    (user_id, fact),
                ).fetchone()
                if not existing:
                    conn.execute(
                        "INSERT INTO facts (user_id, fact) VALUES (?, ?)",
                        (user_id, fact),
                    )
                    logger.info(f"New fact saved: {fact[:50]}...")

    def get_facts(self, user_id: int) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT fact FROM facts WHERE user_id = ? ORDER BY created_at",
                (user_id,),
            ).fetchall()
        return [r[0] for r in rows]

    def get_facts_prompt(self, user_id: int) -> str:
        """Format facts as context for the system prompt."""
        facts = self.get_facts(user_id)
        if not facts:
            return ""
        facts_text = "\n".join(f"- {f}" for f in facts)
        return f"\nKullanici hakkinda bildiklerin:\n{facts_text}\n"
