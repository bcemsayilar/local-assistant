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
            "description": "Spor program tablosuna antrenman kaydi ekle. Mevcut programa yeni tarih satiri ekler.",
            "parameters": {
                "type": "object",
                "properties": {
                    "program": {"type": "string", "description": "Program numarasi veya adi (1, 2, sirt, gogus vb)"},
                    "data": {"type": "string", "description": "Hareket degerleri - Hareket:agirliklar pipe ile ayrilir, agirliklar virgul ile. TUM hareketleri yaz, bahsedilmeyenler icin varsayilan program degerlerini kullan. Ornek: Bench press:25,25,30,35|Makine butterfly:39,34,39,44|Dumble fly:12,12,15,17.5"},
                    "note": {"type": "string", "description": "Genel antrenman notu (opsiyonel)"},
                },
                "required": ["program", "data"],
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


def sport_log(program: str, data: str, note: str = "") -> Dict[str, Any]:
    """Spor program tablosuna antrenman satiri ekler.

    Mevcut program notunu okur, tablo basligindaki hareket sutunlarini bulur,
    data'daki degerleri eslestirir ve yeni tarih satiri ekler.

    program: program numarasi veya adi (1, 2, sirt, gogus vb)
    data: "Hareket:setler|Hareket:setler" formati (ornek: "Bench press:9,7,5,3|Fly:12,12,10")
    note: genel antrenman notu
    """
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")

        # Find program file in spor/ folder
        spor_dir = OBSIDIAN_VAULT / "spor"
        if not spor_dir.exists():
            return {"error": "spor/ klasoru bulunamadi"}

        target = None
        for f in spor_dir.glob("Program*.md"):
            # Extract number from filename and compare
            import re as _re
            num_match = _re.match(r'Program\s*(\d+)', f.stem)
            if num_match and num_match.group(1) == program:
                target = f
                break

        if not target or not target.exists():
            return {"error": f"Program bulunamadi: {program}"}

        content = target.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Find table structure
        header_idx = None
        separator_idx = None
        last_table_idx = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("| Tarih"):
                header_idx = i
            elif header_idx is not None and separator_idx is None and stripped.startswith("|") and set(stripped.replace("|", "").strip()) <= {"-", " "}:
                # Separator: |---|---| or | --- | --- | or | ----- | etc.
                separator_idx = i
            elif separator_idx is not None and stripped.startswith("|") and not (set(stripped.replace("|", "").strip()) <= {"-", " "}):
                # Data row (not empty - skip rows that are only whitespace/pipes)
                row_content = stripped.replace("|", "").strip()
                if row_content:
                    last_table_idx = i
            elif separator_idx is not None and not stripped.startswith("|"):
                break

        if header_idx is None:
            return {"error": "Tablo baslik satiri bulunamadi (| Tarih ile baslamali)"}
        if separator_idx is None:
            return {"error": "Tablo separator satiri bulunamadi (|---|---| formatinda olmali)"}

        # Parse header columns
        headers = [h.strip() for h in lines[header_idx].split("|")]
        headers = [h for h in headers if h]  # Remove empty from split

        # Parse exercise data: "Bench press:9,7,5,3|Fly:12,12,10"
        exercise_map = {}
        for pair in data.split("|"):
            pair = pair.strip()
            if ":" in pair:
                name, values = pair.split(":", 1)
                exercise_map[name.strip().lower()] = values.strip()

        # Match exercise keys to columns (each key matches at most one column)
        column_values = {}
        for ex_key, ex_val in exercise_map.items():
            best_col = None
            best_score = 0
            for header in headers:
                h_lower = header.lower().strip()
                if h_lower in ("tarih", "notlar") or h_lower in column_values:
                    continue
                score = 0
                if ex_key == h_lower:
                    score = 1000  # exact
                elif ex_key in h_lower:
                    score = len(ex_key) * 10  # key substring of column
                elif h_lower in ex_key:
                    score = len(h_lower)  # column substring of key
                else:
                    for word in ex_key.split():
                        if len(word) >= 3 and word in h_lower:
                            score = max(score, len(word))
                # Tiebreaker: prefer shorter column name (closer match)
                if score > best_score or (score == best_score and score > 0 and best_col and len(h_lower) < len(best_col)):
                    best_score = score
                    best_col = h_lower
            if best_col:
                column_values[best_col] = ex_val

        # Build row
        row_cells = []
        for header in headers:
            h_lower = header.lower().strip()
            if h_lower == "tarih":
                row_cells.append(date_str)
            elif h_lower == "notlar":
                # Newlines break markdown tables - replace with <br>
                clean_note = note.replace("\n", "<br>") if note else ""
                row_cells.append(clean_note)
            else:
                row_cells.append(column_values.get(h_lower, "-"))

        new_row = "| " + " | ".join(row_cells) + " |"

        # Insert after last data row, or after separator if table is empty
        insert_idx = (last_table_idx if last_table_idx is not None else separator_idx) + 1
        lines.insert(insert_idx, new_row)

        target.write_text("\n".join(lines), encoding="utf-8")
        return {"success": True, "note": target.stem, "date": date_str}

    except Exception as e:
        return {"error": str(e)}


def dream_log(content: str) -> Dict[str, Any]:
    """Ruya kaydi - tek dosyaya tarihli callout toggle ekler."""
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")

        content_lines = content.split("\n")
        callout_content = "\n> ".join(content_lines)
        formatted = f"> [!note]- Ruya - {date_str}\n> {callout_content}"

        # Find the single dream file in ruya/ folder
        ruya_dir = OBSIDIAN_VAULT / "ruya"
        ruya_file = None
        if ruya_dir.exists():
            md_files = list(ruya_dir.glob("*.md"))
            if md_files:
                ruya_file = md_files[0]  # Use the first (and only) md file

        if ruya_file and ruya_file.exists():
            # Append to existing file
            existing = ruya_file.read_text(encoding="utf-8")
            ruya_file.write_text(existing.rstrip() + "\n\n" + formatted, encoding="utf-8")
            return {"success": True, "note": f"ruya/{ruya_file.stem}", "action": "appended"}
        else:
            # Fallback: create ruya/Ruya.md
            return note_write("ruya/Rüya", formatted)
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
