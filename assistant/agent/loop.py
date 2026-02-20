"""ReAct agent loop - the brain of the assistant."""

import json
import logging
from typing import Dict, Any, Optional

import ollama

from assistant.config import OLLAMA_MODEL, OLLAMA_BASE_URL, MAX_AGENT_ITERATIONS
from assistant.agent.prompts import SYSTEM_PROMPT
from assistant.agent.tools import (
    TOOL_DEFINITIONS,
    safe_shell,
    read_file,
    write_file,
    create_apple_note,
    create_apple_reminder,
)

logger = logging.getLogger(__name__)

# Ollama client
client = ollama.Client(host=OLLAMA_BASE_URL)


async def execute_tool(name: str, args: Dict[str, Any], rag_retriever=None, web_searcher=None) -> Dict[str, Any]:
    """Execute a tool by name and return the result."""
    try:
        if name == "search_documents":
            if rag_retriever:
                results = await rag_retriever.search(args["query"])
                return {"results": results}
            return {"error": "Belge arama henuz kurulmadi"}

        elif name == "read_file":
            return read_file(args["path"])

        elif name == "write_file":
            return write_file(args["path"], args["content"])

        elif name == "web_search":
            if web_searcher:
                results = await web_searcher.search(args["query"])
                return {"results": results}
            return {"error": "Web arama (SearxNG) henuz kurulmadi"}

        elif name == "shell_command":
            return safe_shell(args["command"])

        elif name == "create_note":
            return create_apple_note(args["title"], args["content"])

        elif name == "create_reminder":
            return create_apple_reminder(args["title"])

        else:
            return {"error": f"Bilinmeyen arac: {name}"}
    except Exception as e:
        logger.error(f"Tool execution error ({name}): {e}")
        return {"error": str(e)}


async def agent_loop(
    user_message: str,
    history: list,
    rag_retriever=None,
    web_searcher=None,
) -> str:
    """Run the ReAct agent loop. Returns the final text response."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    messages.append({"role": "user", "content": user_message})

    for iteration in range(MAX_AGENT_ITERATIONS):
        logger.info(f"Agent iteration {iteration + 1}/{MAX_AGENT_ITERATIONS}")

        try:
            response = client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                options={"temperature": 0.3, "num_ctx": 4096},
            )
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return f"LLM hatasi: {e}"

        msg = response.get("message", {})
        content = msg.get("content", "")
        tool_calls = msg.get("tool_calls", [])

        # No tool calls -> final answer
        if not tool_calls:
            return content or "Yanit uretilemedi."

        # Append assistant message with tool calls
        messages.append(msg)

        # Execute each tool call
        for tc in tool_calls:
            func = tc.get("function", {})
            func_name = func.get("name", "unknown")
            func_args = func.get("arguments", {})

            logger.info(f"Tool call: {func_name}({json.dumps(func_args, ensure_ascii=False)[:200]})")

            result = await execute_tool(func_name, func_args, rag_retriever, web_searcher)

            messages.append({
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False, default=str),
            })

    return "Maksimum iterasyon sayisina ulasildi. Istek tamamlanamadi."
