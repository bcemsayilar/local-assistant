"""Tool definitions and executors for the agent."""

import json
import subprocess
import shlex
from pathlib import Path
from typing import Dict, Any

ALLOWED_COMMANDS = {
    "ls", "cat", "find", "grep", "head", "tail", "pwd",
    "date", "cal", "df", "du", "ps", "whoami", "uname", "wc",
}

BLOCKED_PATTERNS = ["rm", "rmdir", "dd", "mkfs", ">", ">>", "|", ";", "&&", "sudo"]

# Tool definitions for Ollama function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Kisisel belgelerde bilgi ara (RAG). Notlar, PDF'ler, markdown dosyalari icerisinde arama yapar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Aranacak metin veya soru"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Dosya icerigini oku",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Dosya yolu (mutlak)"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Dosyaya yaz veya yeni dosya olustur",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Dosya yolu"},
                    "content": {"type": "string", "description": "Yazilacak icerik"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Web'de arama yap (lokal SearxNG uzerinden, gizli)",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Arama sorgusu"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "shell_command",
            "description": "Guvenli, salt okunur kabuk komutu calistir (ls, grep, find, date vb.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Calistirilacak komut"}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_note",
            "description": "Yeni not olustur veya Apple Notes'a kaydet",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Not basligi"},
                    "content": {"type": "string", "description": "Not icerigi"},
                },
                "required": ["title", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "Apple Reminders'a hatirlatma ekle",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Hatirlatma metni"}
                },
                "required": ["title"],
            },
        },
    },
]


def safe_shell(command: str) -> Dict[str, Any]:
    """Execute a whitelisted shell command."""
    try:
        tokens = shlex.split(command)
    except ValueError as e:
        return {"error": f"Komut parse hatasi: {e}"}

    if not tokens:
        return {"error": "Bos komut"}

    base_cmd = tokens[0]
    if base_cmd not in ALLOWED_COMMANDS:
        return {"error": f"Izin verilmeyen komut: {base_cmd}. Izinli: {', '.join(sorted(ALLOWED_COMMANDS))}"}

    for pattern in BLOCKED_PATTERNS:
        if pattern in command:
            return {"error": f"Engellenen kalip: {pattern}"}

    try:
        result = subprocess.run(
            tokens,
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout[:3000] if result.stdout else ""
        error = result.stderr[:500] if result.stderr else ""
        return {"stdout": output, "stderr": error, "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "Komut zaman asimina ugradi (10s)"}
    except Exception as e:
        return {"error": str(e)}


def read_file(path: str) -> Dict[str, Any]:
    """Read a file's contents."""
    try:
        p = Path(path).expanduser()
        if not p.exists():
            return {"error": f"Dosya bulunamadi: {path}"}
        if not p.is_file():
            return {"error": f"Dizin, dosya degil: {path}"}
        content = p.read_text(encoding="utf-8", errors="replace")
        if len(content) > 5000:
            content = content[:5000] + f"\n... ({len(content)} karakter, kisaltildi)"
        return {"content": content, "path": str(p)}
    except Exception as e:
        return {"error": str(e)}


def write_file(path: str, content: str) -> Dict[str, Any]:
    """Write content to a file."""
    try:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"success": True, "path": str(p), "bytes": len(content.encode("utf-8"))}
    except Exception as e:
        return {"error": str(e)}


def create_apple_note(title: str, content: str) -> Dict[str, Any]:
    """Create a note in Apple Notes via osascript."""
    escaped_title = title.replace('"', '\\"')
    escaped_body = content.replace('"', '\\"').replace("\n", "\\n")
    script = f'tell application "Notes"\nmake new note at default account with properties {{name:"{escaped_title}", body:"{escaped_body}"}}\nend tell'
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return {"success": True, "title": title}
        return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def create_apple_reminder(title: str) -> Dict[str, Any]:
    """Create a reminder in Apple Reminders via osascript."""
    escaped = title.replace('"', '\\"')
    script = f'tell application "Reminders"\nset newReminder to make new reminder at end of default list\nset name of newReminder to "{escaped}"\nend tell'
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return {"success": True, "title": title}
        return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}
