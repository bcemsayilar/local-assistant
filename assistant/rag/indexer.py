"""Document indexer - reads, chunks, and stores documents in LanceDB."""

import logging
import sqlite3
from pathlib import Path
from typing import List, Dict
from datetime import datetime

import lancedb

from assistant.config import (
    VECTOR_STORE_DIR,
    MEMORY_DB_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    WATCHED_EXTENSIONS,
)
from assistant.rag.embeddings import get_embeddings

logger = logging.getLogger(__name__)


def read_document(path: Path) -> str:
    """Read document content based on file type."""
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(str(path))
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        except ImportError:
            logger.warning("PyMuPDF not installed, skipping PDF: %s", path)
            return ""

    elif suffix in {".md", ".txt", ".html"}:
        return path.read_text(encoding="utf-8", errors="replace")

    elif suffix == ".docx":
        try:
            import docx

            doc = docx.Document(str(path))
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            logger.warning("python-docx not installed, skipping: %s", path)
            return ""

    return ""


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks."""
    if not text.strip():
        return []

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


class DocumentIndexer:
    """Indexes documents into LanceDB for RAG retrieval."""

    def __init__(self):
        VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(str(VECTOR_STORE_DIR))
        self._ensure_table()

    def _ensure_table(self):
        """Create the documents table if it doesn't exist."""
        if "documents" not in self.db.table_names():
            # Create with a dummy record, then delete it
            import pyarrow as pa

            schema = pa.schema([
                pa.field("text", pa.string()),
                pa.field("source", pa.string()),
                pa.field("chunk_index", pa.int32()),
                pa.field("vector", pa.list_(pa.float32(), 768)),
            ])
            self.db.create_table("documents", schema=schema)

    def index_file(self, path: Path) -> int:
        """Index a single file. Returns number of chunks indexed."""
        if path.suffix.lower() not in WATCHED_EXTENSIONS:
            return 0

        text = read_document(path)
        if not text.strip():
            return 0

        chunks = chunk_text(text)
        if not chunks:
            return 0

        logger.info(f"Indexing {path.name}: {len(chunks)} chunks")

        # Generate embeddings
        embeddings = get_embeddings(chunks)

        # Prepare records
        records = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            records.append({
                "text": chunk,
                "source": str(path),
                "chunk_index": i,
                "vector": emb,
            })

        # Remove old records for this file
        table = self.db.open_table("documents")
        try:
            table.delete(f'source = "{str(path)}"')
        except Exception:
            pass

        # Add new records
        table.add(records)

        # Update SQLite metadata
        self._update_metadata(path, len(chunks))

        return len(chunks)

    def index_directory(self, directory: str) -> Dict[str, int]:
        """Index all supported files in a directory."""
        dir_path = Path(directory).expanduser()
        if not dir_path.is_dir():
            logger.warning(f"Not a directory: {directory}")
            return {}

        results = {}
        for ext in WATCHED_EXTENSIONS:
            for file_path in dir_path.rglob(f"*{ext}"):
                try:
                    count = self.index_file(file_path)
                    if count > 0:
                        results[str(file_path)] = count
                except Exception as e:
                    logger.error(f"Error indexing {file_path}: {e}")

        return results

    def _update_metadata(self, path: Path, chunk_count: int):
        """Update document metadata in SQLite."""
        with sqlite3.connect(MEMORY_DB_PATH) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO documents (path, filename, file_type, chunk_count, indexed_at, modified_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    str(path),
                    path.name,
                    path.suffix,
                    chunk_count,
                    datetime.now().isoformat(),
                    datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                ),
            )
