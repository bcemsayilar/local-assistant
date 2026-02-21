"""ReAct agent loop - the brain of the assistant."""

import json
import logging
import re
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

import ollama

from assistant.config import OLLAMA_MODEL, OLLAMA_BASE_URL, MAX_AGENT_ITERATIONS, GRAPHTHULHU_URL
from assistant.agent.prompts import SYSTEM_PROMPT
from assistant.agent.tools import (
    TOOL_DEFINITIONS,
    MCP_TOOLS,
    MCP_TOOL_MAP,
    MCP_ARG_MAP,
    safe_shell,
    create_apple_reminder,
    note_write,
    note_read,
    note_append,
    note_list,
    note_delete,
    daily_log,
    sport_log,
    dream_log,
)
from assistant.mcp.client import GraphThulhuClient

logger = logging.getLogger(__name__)

# Ollama client
client = ollama.Client(host=OLLAMA_BASE_URL)

# GraphThulhu MCP client (lazy init)
_mcp_client = None


def get_mcp_client():
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = GraphThulhuClient(base_url=GRAPHTHULHU_URL)
    return _mcp_client


async def execute_tool(name: str, args: Dict[str, Any], rag_retriever=None, web_searcher=None) -> Dict[str, Any]:
    """Execute a tool by name and return the result."""
    try:
        # Direct filesystem note tools
        if name == "note_write":
            return note_write(args["name"], args["content"])
        elif name == "note_read":
            return note_read(args["name"])
        elif name == "note_append":
            return note_append(args["name"], args["content"])
        elif name == "note_list":
            return note_list(args.get("folder", ""))
        elif name == "note_delete":
            return note_delete(args["name"])

        # Smart formatting tools
        elif name == "daily_log":
            return daily_log(args["content"])
        elif name == "sport_log":
            return sport_log(args["day"], args["exercises"], args.get("general_note", ""))
        elif name == "dream_log":
            return dream_log(args["content"])

        # MCP graph analysis tools -> GraphThulhu
        elif name in MCP_TOOLS:
            mcp_name = MCP_TOOL_MAP[name]
            mcp_args = MCP_ARG_MAP[name](args)
            result = get_mcp_client().call_tool(mcp_name, mcp_args)
            # Trigger vault reload so GraphThulhu picks up filesystem writes
            return result

        elif name == "search_documents":
            if rag_retriever:
                results = await rag_retriever.search(args["query"])
                return {"results": results}
            return {"error": "Belge arama henuz kurulmadi"}

        elif name == "web_search":
            if web_searcher:
                results = await web_searcher.search(args["query"])
                return {"results": results}
            return {"error": "Web arama (SearxNG) henuz kurulmadi"}

        elif name == "shell_command":
            return safe_shell(args["command"])

        elif name == "create_reminder":
            return create_apple_reminder(args["title"])

        else:
            return {"error": f"Bilinmeyen arac: {name}"}
    except Exception as e:
        logger.error(f"Tool execution error ({name}): {e}")
        return {"error": str(e)}


KNOWN_TOOLS = {
    "note_write", "note_read", "note_append", "note_list", "note_delete",
    "daily_log", "sport_log", "dream_log",
    "vault_search", "vault_links", "vault_overview", "vault_tags",
    "vault_gaps", "vault_clusters", "search_documents", "web_search",
    "shell_command", "create_reminder",
}


def parse_tool_calls_from_text(content: str) -> List[Tuple[str, Dict[str, Any]]]:
    """Parse tool calls that the model wrote as text instead of using function calling.

    Handles patterns like:
    - note_write(name="x", content="y")
    - {"name": "note_write", "arguments": {"name": "x"}}
    - <tool_call>{"name": "note_write", ...}</tool_call>
    """
    calls = []

    # Pattern 1: tool_name(key="value", ...) - function-style
    for tool_name in KNOWN_TOOLS:
        pattern = rf'{tool_name}\s*\(\s*(.*?)\s*\)'
        for match in re.finditer(pattern, content, re.DOTALL):
            args_str = match.group(1)
            args = {}
            # Parse key="value" or key='value' pairs
            for kv in re.finditer(r'(\w+)\s*=\s*["\'](.+?)["\']', args_str, re.DOTALL):
                args[kv.group(1)] = kv.group(2)
            if args:
                calls.append((tool_name, args))

    if calls:
        return calls

    # Pattern 2: JSON with "name" and "arguments" keys
    json_blocks = re.findall(r'\{[^{}]*"name"\s*:\s*"(\w+)"[^{}]*"arguments"\s*:\s*(\{[^{}]*\})[^{}]*\}', content, re.DOTALL)
    for name, args_json in json_blocks:
        if name in KNOWN_TOOLS:
            try:
                args = json.loads(args_json)
                calls.append((name, args))
            except json.JSONDecodeError:
                pass

    if calls:
        return calls

    # Pattern 3: <tool_call> tags
    tool_call_blocks = re.findall(r'<tool_call>\s*(\{.*?\})\s*</tool_call>', content, re.DOTALL)
    for block in tool_call_blocks:
        try:
            data = json.loads(block)
            name = data.get("name", "")
            args = data.get("arguments", data.get("parameters", {}))
            if name in KNOWN_TOOLS:
                calls.append((name, args))
        except json.JSONDecodeError:
            pass

    return calls


async def agent_loop(
    user_message: str,
    history: list,
    rag_retriever=None,
    web_searcher=None,
) -> str:
    """Run the ReAct agent loop. Returns the final text response."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    messages.append({"role": "user", "content": user_message})

    # ── Prefix routing: direct bypass for dream notes ──
    msg_lower = user_message.lower().strip()
    for prefix in ["rüya notu", "ruya notu"]:
        if msg_lower.startswith(prefix):
            raw = user_message[len(prefix):].strip().lstrip(":").strip()
            if raw:
                result = dream_log(raw)
                if result.get("success"):
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    return f"Ruya notun kaydedildi - ruya/{date_str}"
                return f"Ruya notu kaydedilemedi - {result.get('error', 'bilinmeyen hata')}"
            break

    tool_call_history = []

    for iteration in range(MAX_AGENT_ITERATIONS):
        logger.info(f"Agent iteration {iteration + 1}/{MAX_AGENT_ITERATIONS}")

        # Check for repeated tool calls
        force_text = False
        if len(tool_call_history) >= 2:
            last_two = [t[0] for t in tool_call_history[-2:]]
            if last_two[0] == last_two[1]:
                logger.warning(f"Tool '{last_two[0]}' called 2x in a row - forcing text response")
                force_text = True

        try:
            response = client.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                tools=[] if force_text else TOOL_DEFINITIONS,
                options={"temperature": 0.3, "num_ctx": 4096},
            )
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return f"LLM hatasi: {e}"

        msg = response.get("message", {})
        content = msg.get("content", "")
        tool_calls = msg.get("tool_calls", [])

        logger.info(f"LLM response - tool_calls: {len(tool_calls)}, content_len: {len(content)}, content_preview: {content[:200] if content else '(empty)'}")

        if not tool_calls:
            # Fallback: parse tool calls from text (qwen3:4b sometimes writes them as text)
            parsed = parse_tool_calls_from_text(content) if content else []
            if parsed:
                logger.info(f"Parsed {len(parsed)} tool call(s) from text response")
                for func_name, func_args in parsed:
                    logger.info(f"Text-parsed tool call: {func_name}({json.dumps(func_args, ensure_ascii=False)[:200]})")
                    result = await execute_tool(func_name, func_args, rag_retriever, web_searcher)
                    tool_call_history.append((func_name, iteration))
                    result_str = json.dumps(result, ensure_ascii=False, default=str)
                    if result.get("success") or (isinstance(result.get("result"), str) and "error" not in result):
                        result_str += "\n\n[ISLEM BASARILI - Kullaniciya sonucu bildir, tekrar ayni araci cagirma]"
                    messages.append({"role": "assistant", "content": content})
                    messages.append({"role": "user", "content": f"Arac sonucu: {result_str}\n\nKullaniciya kisa ve anlasilir bir ozet ver."})
                # Get summary from model
                try:
                    summary_resp = client.chat(
                        model=OLLAMA_MODEL,
                        messages=messages,
                        tools=[],
                        options={"temperature": 0.3, "num_ctx": 4096},
                    )
                    summary = summary_resp.get("message", {}).get("content", "")
                    if summary:
                        return summary
                except Exception:
                    pass
                return "Islem tamamlandi."
            return content or "Yanit uretilemedi."

        messages.append(msg)

        for tc in tool_calls:
            func = tc.get("function", {})
            func_name = func.get("name", "unknown")
            func_args = func.get("arguments", {})

            logger.info(f"Tool call: {func_name}({json.dumps(func_args, ensure_ascii=False)[:200]})")

            result = await execute_tool(func_name, func_args, rag_retriever, web_searcher)

            tool_call_history.append((func_name, iteration))

            result_str = json.dumps(result, ensure_ascii=False, default=str)
            if result.get("success") or (isinstance(result.get("result"), str) and "error" not in result):
                result_str += "\n\n[ISLEM BASARILI - Kullaniciya sonucu bildir, tekrar ayni araci cagirma]"

            messages.append({
                "role": "tool",
                "content": result_str,
            })

    # Fallback text-only call
    logger.warning("Max iterations reached - final text-only call")
    try:
        messages.append({
            "role": "user",
            "content": "[Sistem: Arac cagrilari tamamlandi. Lutfen kullaniciya kisa bir ozet ver.]",
        })
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=[],
            options={"temperature": 0.3, "num_ctx": 4096},
        )
        final = response.get("message", {}).get("content", "")
        if final:
            return final
    except Exception:
        pass

    return "Islem tamamlandi ancak ozet olusturulamadi."
