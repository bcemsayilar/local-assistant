"""Claude Code bridge: routes selected Telegram messages to `claude -p` on this machine.

Plain text stays with the local model (qwen via agent_loop). Messages starting with
"claude", photos, videos, documents and voice notes come here. Data sent here leaves
the machine (Anthropic API); that is the deliberate split.
"""

import asyncio
import json
import logging
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

HOME = Path.home()
CLAUDE_BIN = shutil.which("claude") or str(HOME / ".local/bin/claude")
WHISPER_BIN = shutil.which("whisper-cli") or "/opt/homebrew/bin/whisper-cli"
FFMPEG_BIN = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
WHISPER_MODEL = HOME / ".cache/whisper/ggml-large-v3-turbo-q5_0.bin"
INBOX_DIR = HOME / "telegram-inbox"
SESSIONS_FILE = Path(__file__).resolve().parents[2] / "data" / "claude_sessions.json"
TIMEOUT_S = 1800

PREFIX_RE = re.compile(r"^\s*claude\b[\s,:.\-]*", re.IGNORECASE)

SYSTEM_NOTE = (
    "Bu mesaj Telegram'dan, Burak'tan geliyor; Mac Air (ev sunucusu) uzerinde calisiyorsun. "
    "Once ~/CLAUDE.md haritasina bak. Cevabin Telegram'da okunacak: kisa, Turkce, duz metin, "
    "tablo ve uzun markdown yok. Geri donusu olmayan islerde (silme, gonderme, satin alma) "
    "once ne yapacagini yaz ve onay iste, onay bu sohbette gelirse yap."
)


def strip_prefix(text: str):
    """Return the message without the 'claude' prefix, or None if it has no prefix."""
    m = PREFIX_RE.match(text or "")
    if not m:
        return None
    return text[m.end():].strip() or "Merhaba"


def _load_sessions() -> dict:
    try:
        return json.loads(SESSIONS_FILE.read_text())
    except Exception:
        return {}


def _save_sessions(data: dict):
    SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSIONS_FILE.write_text(json.dumps(data))


def reset_session(user_id: int):
    data = _load_sessions()
    data.pop(str(user_id), None)
    _save_sessions(data)


def inbox_path(suffix: str) -> Path:
    day = INBOX_DIR / datetime.now().strftime("%Y-%m-%d")
    day.mkdir(parents=True, exist_ok=True)
    return day / f"{datetime.now().strftime('%H%M%S')}{suffix}"


async def transcribe(audio_path: Path) -> str:
    """Voice note -> text with local whisper. Returns '' if whisper is not available."""
    if not (Path(WHISPER_BIN).exists() and WHISPER_MODEL.exists()):
        return ""
    wav = audio_path.with_suffix(".wav")
    p = await asyncio.create_subprocess_exec(
        FFMPEG_BIN, "-v", "error", "-y", "-i", str(audio_path), "-ar", "16000", "-ac", "1", str(wav)
    )
    await p.wait()
    p = await asyncio.create_subprocess_exec(
        WHISPER_BIN, "-m", str(WHISPER_MODEL), "-f", str(wav), "-l", "auto", "-nt", "-np",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
    )
    out, _ = await p.communicate()
    return out.decode("utf-8", "replace").strip()


async def ask_claude(user_id: int, prompt: str) -> str:
    """Run one turn of Claude Code, resuming this user's session."""
    sessions = _load_sessions()
    sid = sessions.get(str(user_id))
    cmd = [
        CLAUDE_BIN, "-p", f"{SYSTEM_NOTE}\n\n{prompt}",
        "--output-format", "json",
        "--dangerously-skip-permissions",
    ]
    if sid:
        cmd += ["--resume", sid]
    env = dict(os.environ)
    env.setdefault("PATH", "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin")
    env["PATH"] = f"{HOME}/.local/bin:/opt/homebrew/bin:{env['PATH']}"
    proc = await asyncio.create_subprocess_exec(
        *cmd, cwd=str(HOME), env=env,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    try:
        out, err = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT_S)
    except asyncio.TimeoutError:
        proc.kill()
        return f"Claude {TIMEOUT_S // 60} dakikada bitiremedi, is yarida kaldi."
    if proc.returncode != 0 and not out:
        logger.error(f"claude failed: {err.decode()[:500]}")
        if sid:  # stale session id, start fresh next time
            reset_session(user_id)
        return f"Claude hata verdi: {err.decode()[:300]}"
    try:
        data = json.loads(out.decode())
    except json.JSONDecodeError:
        return out.decode()[:4000]
    if data.get("session_id"):
        sessions[str(user_id)] = data["session_id"]
        _save_sessions(sessions)
    return data.get("result") or "(bos cevap)"
