"""Anahtar kelimeyle baslayan Telegram mesajlarini Obsidian vault'a yazar. Model yok, sadece kod (kurucu karari 2026-10-23).

  ruya ...    -> ruya/<tek dosya>.md, tarihli callout
  gunluk ...  -> gunluk/YYYY-MM-DD.md, saatli callout
  spor 1 ...  -> spor/Program 1*.md tablosuna bugunun satiri (numarasiz 'spor ...' Claude'a gider)

route(text) eslesme yoksa None doner, mesaj Claude'a gider.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from assistant.config import OBSIDIAN_VAULT as _VAULT_STR

OBSIDIAN_VAULT = Path(_VAULT_STR).expanduser()

PREFIX = re.compile(r"^\s*(rüya|ruya|günlük|gunluk|spor)(?:\s+not(?:u|um)?)?\s*[:\-,.]?\s*(.*)$", re.I | re.S)
KIND = {"rüya": "ruya", "ruya": "ruya", "günlük": "gunluk", "gunluk": "gunluk", "spor": "spor"}


def _callout(title: str, content: str) -> str:
    return f"> [!note]- {title}\n> " + "\n> ".join(content.strip().split("\n"))


def _append(p: Path, block: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    old = p.read_text(encoding="utf-8").rstrip() + "\n\n" if p.exists() else ""
    p.write_text(old + block + "\n", encoding="utf-8")


def daily_log(content: str) -> Dict[str, Any]:
    now = datetime.now()
    p = OBSIDIAN_VAULT / "gunluk" / f"{now:%Y-%m-%d}.md"
    _append(p, _callout(f"{now:%H:%M}", content))
    return {"note": f"gunluk/{p.stem}"}


def dream_log(content: str) -> Dict[str, Any]:
    d = OBSIDIAN_VAULT / "ruya"
    files = sorted(d.glob("*.md")) if d.exists() else []
    p = files[0] if files else d / "Rüya.md"
    _append(p, _callout(f"Ruya - {datetime.now():%Y-%m-%d}", content))
    return {"note": f"ruya/{p.stem}"}


PROGRAM_DEFAULTS = {
    "1": {
        "pull down": "29,34,39,44",
        "enseye cekis": "29,34,39,44",
        "dar tutus goguse cekis": "29,34,39,44",
        "omuz trapez": "10,12.5,12.5,15",
        "sikistirma trapez": "10,10,12.5,12.5",
        "dumble yana acis": "10,10,10,10",
        "on omuz": "7.5,7.5,7.5,7.5",
        "alna indiris": "5,5,10,10",
        "push down": "15,15,15,17",
        "ip yana acis": "12.5,12.5,12.5,15",
        "mekik": "150",
        "kosu": "300m yuruyus + 700-800m kosu + 300m yuruyus",
    },
    "2": {
        "bench press": "25,25,30,35",
        "fly": "39,34,39,44",
        "dumble fly": "12,12,15,17.5",
        "flower": "10,10,10,10",
        "ayakta dumble biceps": "10,10,10,12.5",
        "ayakta z bar": "10,10,15,15",
        "oturarak z bar": "10,10,12.5,12.5",
        "mekik": "150",
        "kosu": "300m yuruyus + 700-800m kosu + 300m yuruyus",
    },
}


def _is_sep(s: str) -> bool:
    return s.startswith("|") and set(s.replace("|", "").strip()) <= {"-", " ", ":"}


def sport_log(program: str, exercises: Dict[str, str], note: str = "") -> Dict[str, Any]:
    """Program tablosuna bugunun satirini ekler. Verilmeyen hareket program varsayilaniyla, o da yoksa '-' ile dolar."""
    d = OBSIDIAN_VAULT / "spor"
    target = next((f for f in d.glob("Program*.md") if re.match(rf"Program\s*{program}\b", f.stem)), None) if d.exists() else None
    if not target:
        return {"error": f"Program bulunamadi: {program} (spor/Program {program} ... .md)"}
    lines = target.read_text(encoding="utf-8").split("\n")
    head = sep = last = None
    for i, l in enumerate(lines):
        s = l.strip()
        if head is None and s.startswith("| Tarih"):
            head = i
        elif head is not None and sep is None and _is_sep(s):
            sep = i
        elif sep is not None and s.startswith("|") and s.replace("|", "").strip():
            last = i
        elif sep is not None and not s.startswith("|"):
            break
    if head is None or sep is None:
        return {"error": "Tablo bulunamadi (| Tarih ile baslayan baslik ve ayirici satir gerekir)"}
    cols = [c.strip() for c in lines[head].split("|") if c.strip()]
    lower = [c.lower() for c in cols]
    vals: Dict[str, str] = {}
    unknown = []
    for k, v in exercises.items():
        # once tam ad, sonra kolon adinin parcasi; her kolon bir kez
        hit = next((c for c in lower if c == k), None) or next((c for c in lower if k in c and c not in vals), None) \
            or next((c for c in lower if c in k and c not in ("tarih", "notlar") and c not in vals), None)
        if hit and hit not in ("tarih", "notlar"):
            vals[hit] = v
        else:
            unknown.append(k)
    defaults = PROGRAM_DEFAULTS.get(program, {})
    row = []
    for c in lower:
        if c == "tarih":
            row.append(f"{datetime.now():%Y-%m-%d}")
        elif c == "notlar":
            row.append(note.replace("\n", "<br>"))
        else:
            row.append(vals.get(c) or defaults.get(c, "-"))
    lines.insert((last if last is not None else sep) + 1, "| " + " | ".join(row) + " |")
    target.write_text("\n".join(lines), encoding="utf-8")
    return {"note": f"spor/{target.stem}", "unknown": unknown}


def _parse_sport(body: str):
    """'1\\nbench press: 30,30\\nfly: 12' ya da '1 bench press: 30,30; fly: 12 iyi gecti' -> ('1', {...}, not)."""
    m = re.match(r"\s*(?:program\s*)?(\d+)\s*[:\-,.]?\s*(.*)$", body, re.I | re.S)
    if not m:
        return None
    program, rest = m.group(1), m.group(2)
    ex, note = {}, []
    for part in re.split(r"[\n;|]", rest):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            k, v = part.split(":", 1)
            ex[k.strip().lower()] = v.strip()
        else:
            note.append(part)
    return program, ex, " ".join(note)


def route(text: str) -> Optional[Dict[str, Any]]:
    """Anahtar kelimeyle baslayan mesaji kaydeder. Eslesme yoksa None. Donus: {'kind', 'reply'}."""
    m = PREFIX.match(text or "")
    if not m:
        return None
    kind, body = KIND[m.group(1).lower()], m.group(2).strip()
    if kind == "spor" and not _parse_sport(body):
        return None  # "spor salonu..." gibi program numarasiz metin not degil, Claude'a gider
    if not body:
        return {"kind": kind, "reply": "Bos not kaydedilmedi."}
    try:
        if kind == "ruya":
            return {"kind": kind, "reply": f"Kaydedildi: {dream_log(body)['note']}"}
        if kind == "gunluk":
            return {"kind": kind, "reply": f"Kaydedildi: {daily_log(body)['note']}"}
        r = sport_log(*_parse_sport(body))
        if "error" in r:
            return {"kind": kind, "reply": r["error"]}
        extra = f"\nTabloda bulunamayan: {', '.join(r['unknown'])}" if r["unknown"] else ""
        return {"kind": kind, "reply": f"Kaydedildi: {r['note']}{extra}"}
    except Exception as e:
        return {"kind": kind, "reply": f"Kaydedilemedi: {e}"}
