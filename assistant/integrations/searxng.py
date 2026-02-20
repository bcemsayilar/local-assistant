"""SearxNG web search client - private, local meta-search."""

import logging
from typing import List, Dict, Any

import httpx

from assistant.config import SEARXNG_URL

logger = logging.getLogger(__name__)


class WebSearcher:
    """Searches the web privately via a local SearxNG instance."""

    def __init__(self, base_url: str = SEARXNG_URL):
        self.base_url = base_url.rstrip("/")
        self.search_url = f"{self.base_url}/search"

    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Perform a web search and return results."""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(
                    self.search_url,
                    params={
                        "q": query,
                        "format": "json",
                        "language": "tr-TR",
                        "categories": "general",
                    },
                )
                response.raise_for_status()
                data = response.json()

            results = []
            for item in data.get("results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", "")[:500],
                })
            return results

        except httpx.ConnectError:
            logger.warning("SearxNG not reachable at %s", self.base_url)
            return [{"error": "SearxNG baglantisi kurulamadi. Docker container calistigindan emin olun."}]
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return [{"error": str(e)}]
