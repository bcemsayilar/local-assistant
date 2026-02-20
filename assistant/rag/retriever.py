"""RAG retriever - searches indexed documents via LanceDB."""

import logging
from typing import List, Dict, Any

import lancedb

from assistant.config import VECTOR_STORE_DIR
from assistant.rag.embeddings import get_embedding

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Searches the vector store for relevant document chunks."""

    def __init__(self):
        self.db = lancedb.connect(str(VECTOR_STORE_DIR))

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant chunks matching the query."""
        if "documents" not in self.db.table_names():
            return []

        table = self.db.open_table("documents")

        if table.count_rows() == 0:
            return []

        try:
            query_embedding = get_embedding(query)
            results = (
                table.search(query_embedding)
                .limit(top_k)
                .to_list()
            )

            return [
                {
                    "text": r["text"],
                    "source": r["source"],
                    "score": 1 - r.get("_distance", 0),
                }
                for r in results
            ]
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
