"""Tool definitions and executors for the agent."""

import json
import subprocess
import shlex
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from assistant.config import OBSIDIAN_VAULT as _VAULT_STR

OBSIDIAN_VAULT = Path(_VAULT_STR).expanduser()

ALLOWED_COMMANDS = {
    "ls", "cat", "find", "grep", "head", "tail", "pwd",
    "date", "cal", "df", "du", "ps", "whoami", "uname", "wc",
}

BLOCKED_PATTERNS = ["rm", "rmdir", "dd", "mkfs", ">", ">>", "|", ";", "&&", "sudo"]

# ── MCP tool names routed to GraphThulhu (read/analysis only) ──
MCP_TOOLS = {
    "vault_search", "vault_links", "vault_overview",
    "vault_tags", "vault_gaps", "vault_clusters",
}

# ── Tool definitions for Ollama function calling ──
TOOL_DEFINITIONS = [
    # --- Obsidian write tools (direct filesystem, clean markdown) ---
    {
        "type": "function",
        "function": {
            "name": "note_write",
            "description": "Obsidian'da not olustur veya guncelle. Temiz markdown yazar. Klasor icin / kullan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Not adi (ornek: spor/program1 veya gunluk/2026-02-21)"},
                    "content": {"type": "string", "description": "Markdown icerik"},
                },
                "required": ["name", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "note_read",
            "description": "Obsidian'dan not oku.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Not adi"},
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "note_append",
            "description": "Notun sonuna icerik ekle. Gunluk log, spor takibi icin ideal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Not adi"},
                    "content": {"type": "string", "description": "Eklenecek markdown icerik"},
                },
                "required": ["name", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "note_list",
            "description": "Vault'taki notlari ve klasorleri listele.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder": {"type": "string", "description": "Klasor (bos = tum vault)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "note_delete",
            "description": "Obsidian notu sil.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Silinecek not adi"},
                },
                "required": ["name"],
            },
        },
    },
    # --- Smart formatting tools (Python handles all markdown) ---
    {
        "type": "function",
        "function": {
            "name": "daily_log",
            "description": "Gunluk nota zaman damgali kayit ekle. gunluk/YYYY-MM-DD.md dosyasina yazar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Kaydedilecek metin"},
                },
                "required": ["content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sport_log",
            "description": "Spor antrenman kaydi. spor/{day}.md dosyasina tablo olarak yazar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {"type": "string", "description": "Antrenman turu (push-day, pull-day, leg-day vb)"},
                    "exercises": {"type": "string", "description": "Hareketler pipe ile ayrilmis: Hareket|SetxTekrar|Agirlik|Not - satirlar \\n ile ayrilir"},
                    "general_note": {"type": "string", "description": "Genel antrenman notu (opsiyonel)"},
                },
                "required": ["day", "exercises"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dream_log",
            "description": "Ruya kaydi. ruya/YYYY-MM-DD.md dosyasina callout formatinda yazar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Ruya icerigi"},
                },
                "required": ["content"],
            },
        },
    },
    # --- GraphThulhu MCP tools (graph analysis, search) ---
    {
        "type": "function",
        "function": {
            "name": "vault_search",
            "description": "Vault'ta tam metin arama. Tum notlarda arar, eslesen bloklari dondurur.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Aranacak metin"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_links",
            "description": "Sayfanin baglantilari - ileri linkler ve geri linkler (backlinks).",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Sayfa adi"},
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_overview",
            "description": "Bilgi grafigi ozeti - toplam sayfa, link, en bagli sayfalar, orphanlar.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_tags",
            "description": "Belirli bir tag'e sahip tum notlari bul.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag": {"type": "string", "description": "Aranacak tag"},
                },
                "required": ["tag"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_gaps",
            "description": "Bilgi grafigindeki bosluklar - orphan sayfalar, dead-end, zayif baglanti.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "vault_clusters",
            "description": "Konu kumeleri - birbirine bagli sayfa gruplari ve hub'lar.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    # --- Non-Obsidian tools ---
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Kisisel belgelerde bilgi ara (RAG).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Aranacak metin"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Web'de arama yap (SearxNG, gizli).",
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
            "description": "Guvenli kabuk komutu (ls, grep, find, date vb.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Komut"}
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_reminder",
            "description": "Apple Reminders hatirlatma ekle.",
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

# ── MCP tool name mapping (our name -> GraphThulhu name) ──
MCP_TOOL_MAP = {
    "vault_search": "search",
    "vault_links": "get_links",
    "vault_overview": "graph_overview",
    "vault_tags": "find_by_tag",
    "vault_gaps": "knowledge_gaps",
    "vault_clusters": "topic_clusters",
}

# ── MCP argument mapping ──
MCP_ARG_MAP = {
    "vault_search": lambda args: {"query": args["query"], "compact": True},
    "vault_links": lambda args: {"name": args["name"]},
    "vault_overview": lambda args: {},
    "vault_tags": lambda args: {"tag": args["tag"]},
    "vault_gaps": lambda args: {},
    "vault_clusters": lambda args: {},
}


# ── Direct filesystem Obsidian functions ──

def _vault_path(name: str) -> Path:
    if not name.endswith(".md"):
        name += ".md"
    return OBSIDIAN_VAULT / name


def note_write(name: str, content: str) -> Dict[str, Any]:
    try:
        p = _vault_path(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"success": True, "note": name, "path": str(p)}
    except Exception as e:
        return {"error": str(e)}


def note_read(name: str) -> Dict[str, Any]:
    try:
        p = _vault_path(name)
        if not p.exists():
            return {"error": f"Not bulunamadi: {name}"}
        content = p.read_text(encoding="utf-8")
        if len(content) > 4000:
            content = content[:4000] + f"\n... ({len(content)} karakter, kisaltildi)"
        return {"content": content, "note": name}
    except Exception as e:
        return {"error": str(e)}


def note_append(name: str, content: str) -> Dict[str, Any]:
    try:
        p = _vault_path(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            existing = p.read_text(encoding="utf-8")
            p.write_text(existing.rstrip() + "\n\n" + content, encoding="utf-8")
            return {"success": True, "note": name, "action": "appended"}
        else:
            p.write_text(content, encoding="utf-8")
            return {"success": True, "note": name, "action": "created"}
    except Exception as e:
        return {"error": str(e)}


def note_list(folder: str = "") -> Dict[str, Any]:
    try:
        base = OBSIDIAN_VAULT / folder if folder else OBSIDIAN_VAULT
        if not base.exists():
            return {"error": f"Klasor bulunamadi: {folder}"}
        notes = []
        dirs = []
        for item in sorted(base.iterdir()):
            if item.name.startswith("."):
                continue
            if item.is_dir():
                count = len(list(item.rglob("*.md")))
                dirs.append(f"{item.name}/ ({count} not)")
            elif item.suffix == ".md":
                notes.append(item.stem)
        return {"folders": dirs, "notes": notes}
    except Exception as e:
        return {"error": str(e)}


def note_delete(name: str) -> Dict[str, Any]:
    try:
        p = _vault_path(name)
        if not p.exists():
            return {"error": f"Not bulunamadi: {name}"}
        p.unlink()
        return {"success": True, "note": name}
    except Exception as e:
        return {"error": str(e)}


# ── Smart formatting tools (Python handles all markdown) ──

def daily_log(content: str) -> Dict[str, Any]:
    """Gunluk nota zaman damgali callout toggle ekle."""
    try:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        name = f"gunluk/{date_str}"

        content_lines = content.split("\n")
        callout_content = "\n> ".join(content_lines)
        formatted = f"> [!note]- {time_str}\n> {callout_content}"

        p = _vault_path(name)
        if p.exists():
            return note_append(name, formatted)
        else:
            return note_write(name, formatted)
    except Exception as e:
        return {"error": str(e)}


def sport_log(day: str, exercises: str, general_note: str = "") -> Dict[str, Any]:
    """Spor antrenman kaydi - pipe formatindan markdown tablo uretir."""
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")
        name = f"spor/{day}"

        lines = []
        lines.append(f"## {date_str}")
        lines.append("")
        lines.append("| Hareket | Set x Tekrar | Agirlik | Not |")
        lines.append("|---------|-------------|---------|-----|")

        # Handle both real newlines and literal \n
        rows = exercises.split("\n")
        if len(rows) <= 1:
            rows = exercises.split("\\n")
        rows = [r.strip() for r in rows if r.strip()]

        for row in rows:
            parts = [p.strip() for p in row.split("|")]
            while len(parts) < 4:
                parts.append("")
            parts = parts[:4]
            lines.append(f"| {parts[0]} | {parts[1]} | {parts[2]} | {parts[3]} |")

        if general_note:
            lines.append("")
            lines.append(f"> Genel: {general_note}")

        formatted = "\n".join(lines)

        p = _vault_path(name)
        if p.exists():
            return note_append(name, formatted)
        else:
            return note_write(name, formatted)
    except Exception as e:
        return {"error": str(e)}


def dream_log(content: str) -> Dict[str, Any]:
    """Ruya kaydi - callout toggle formatinda."""
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")
        name = f"ruya/{date_str}"

        content_lines = content.split("\n")
        callout_content = "\n> ".join(content_lines)
        formatted = f"> [!note]- Ruya - {date_str}\n> {callout_content}"

        p = _vault_path(name)
        if p.exists():
            return note_append(name, formatted)
        else:
            return note_write(name, formatted)
    except Exception as e:
        return {"error": str(e)}


# ── Other tool functions ──

def safe_shell(command: str) -> Dict[str, Any]:
    try:
        tokens = shlex.split(command)
    except ValueError as e:
        return {"error": f"Komut parse hatasi: {e}"}
    if not tokens:
        return {"error": "Bos komut"}
    base_cmd = tokens[0]
    if base_cmd not in ALLOWED_COMMANDS:
        return {"error": f"Izin verilmeyen komut: {base_cmd}"}
    for pattern in BLOCKED_PATTERNS:
        if pattern in command:
            return {"error": f"Engellenen kalip: {pattern}"}
    try:
        result = subprocess.run(tokens, capture_output=True, text=True, timeout=10)
        output = result.stdout[:3000] if result.stdout else ""
        error = result.stderr[:500] if result.stderr else ""
        return {"stdout": output, "stderr": error, "returncode": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "Komut zaman asimi (10s)"}
    except Exception as e:
        return {"error": str(e)}


def create_apple_reminder(title: str) -> Dict[str, Any]:
    escaped = title.replace('"', '\\"')
    script = f'tell application "Reminders"\nset newReminder to make new reminder at end of default list\nset name of newReminder to "{escaped}"\nend tell'
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return {"success": True, "title": title}
        return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}
