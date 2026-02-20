"""File system watcher for automatic document re-indexing."""

import logging
import asyncio
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from assistant.config import WATCHED_DIRS, WATCHED_EXTENSIONS
from assistant.rag.indexer import DocumentIndexer

logger = logging.getLogger(__name__)


class DocumentHandler(FileSystemEventHandler):
    """Handles file system events for document changes."""

    def __init__(self, indexer: DocumentIndexer):
        self.indexer = indexer
        self._pending = set()

    def _should_index(self, path: str) -> bool:
        return Path(path).suffix.lower() in WATCHED_EXTENSIONS

    def on_created(self, event):
        if not event.is_directory and self._should_index(event.src_path):
            logger.info(f"New file detected: {event.src_path}")
            self._index(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and self._should_index(event.src_path):
            logger.info(f"File modified: {event.src_path}")
            self._index(event.src_path)

    def _index(self, path: str):
        try:
            count = self.indexer.index_file(Path(path))
            logger.info(f"Indexed {path}: {count} chunks")
        except Exception as e:
            logger.error(f"Index error for {path}: {e}")


def start_watcher(indexer: DocumentIndexer) -> Observer:
    """Start watching configured directories for changes."""
    observer = Observer()
    handler = DocumentHandler(indexer)

    for dir_path in WATCHED_DIRS:
        expanded = Path(dir_path).expanduser()
        if expanded.is_dir():
            observer.schedule(handler, str(expanded), recursive=True)
            logger.info(f"Watching directory: {expanded}")
        else:
            logger.warning(f"Watch directory not found: {dir_path}")

    observer.start()
    return observer


async def initial_index(indexer: DocumentIndexer):
    """Index all documents in watched directories on startup."""
    for dir_path in WATCHED_DIRS:
        expanded = Path(dir_path).expanduser()
        if expanded.is_dir():
            logger.info(f"Initial indexing: {expanded}")
            results = indexer.index_directory(str(expanded))
            total = sum(results.values())
            logger.info(f"Indexed {len(results)} files, {total} chunks from {expanded}")
