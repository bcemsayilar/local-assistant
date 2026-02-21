"""GraphThulhu MCP client over HTTP (Streamable HTTP transport)."""

import json
import logging
from typing import Dict, Any, Optional

import httpx

logger = logging.getLogger(__name__)


class GraphThulhuClient:
    """Connects to GraphThulhu MCP server via HTTP."""

    def __init__(self, base_url: str = "http://localhost:8585"):
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/mcp"
        self.session_id = None
        self._request_id = 0
        self._initialized = False

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _parse_sse(self, text: str) -> Optional[Dict]:
        """Parse SSE response to extract JSON data."""
        for line in text.strip().splitlines():
            if line.startswith("data: "):
                try:
                    return json.loads(line[6:])
                except json.JSONDecodeError:
                    continue
        return None

    def initialize(self) -> bool:
        """Initialize MCP session."""
        try:
            with httpx.Client(timeout=10) as client:
                # Step 1: initialize
                resp = client.post(
                    self.endpoint,
                    json={
                        "jsonrpc": "2.0",
                        "id": self._next_id(),
                        "method": "initialize",
                        "params": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {},
                            "clientInfo": {"name": "local-assistant", "version": "1.0"},
                        },
                    },
                )
                self.session_id = resp.headers.get("mcp-session-id")
                if not self.session_id:
                    logger.error("No session ID in initialize response")
                    return False

                # Step 2: send initialized notification
                client.post(
                    self.endpoint,
                    headers={"Mcp-Session-Id": self.session_id},
                    json={
                        "jsonrpc": "2.0",
                        "method": "notifications/initialized",
                    },
                )
                self._initialized = True
                logger.info(f"GraphThulhu MCP initialized (session={self.session_id[:8]}...)")
                return True
        except Exception as e:
            logger.error(f"GraphThulhu initialize failed: {e}")
            return False

    def call_tool(self, name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call an MCP tool and return the result."""
        if not self._initialized:
            if not self.initialize():
                return {"error": "MCP baglantisi kurulamadi"}

        try:
            with httpx.Client(timeout=30) as client:
                resp = client.post(
                    self.endpoint,
                    headers={"Mcp-Session-Id": self.session_id},
                    json={
                        "jsonrpc": "2.0",
                        "id": self._next_id(),
                        "method": "tools/call",
                        "params": {
                            "name": name,
                            "arguments": arguments or {},
                        },
                    },
                )
                data = self._parse_sse(resp.text)
                if not data:
                    return {"error": f"Bos MCP yaniti: {resp.text[:200]}"}

                if "error" in data:
                    return {"error": data["error"].get("message", str(data["error"]))}

                result = data.get("result", {})
                # MCP returns content as array of {type, text} objects
                content_parts = result.get("content", [])
                texts = []
                for part in content_parts:
                    if isinstance(part, dict) and part.get("text"):
                        texts.append(part["text"])
                    elif isinstance(part, str):
                        texts.append(part)

                combined = "\n".join(texts)
                # Truncate large responses for qwen3:4b context
                if len(combined) > 3000:
                    combined = combined[:3000] + "\n... (kisaltildi)"
                return {"result": combined}

        except httpx.TimeoutException:
            return {"error": "GraphThulhu zaman asimi (30s)"}
        except Exception as e:
            # Session might have expired, retry once
            if "session" in str(e).lower() or "404" in str(e):
                self._initialized = False
                return self.call_tool(name, arguments)
            logger.error(f"MCP call error ({name}): {e}")
            return {"error": str(e)}

    def health_check(self) -> bool:
        """Quick check if GraphThulhu is reachable."""
        try:
            result = self.call_tool("health")
            return "error" not in result
        except Exception:
            return False
