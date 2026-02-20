"""Embedding generation via Ollama (nomic-embed-text)."""

import logging
from typing import List

import ollama

from assistant.config import OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL

logger = logging.getLogger(__name__)

client = ollama.Client(host=OLLAMA_BASE_URL)


def get_embedding(text: str) -> List[float]:
    """Generate embedding for a single text using Ollama."""
    response = client.embed(model=OLLAMA_EMBED_MODEL, input=text)
    return response["embeddings"][0]


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts."""
    response = client.embed(model=OLLAMA_EMBED_MODEL, input=texts)
    return response["embeddings"]
