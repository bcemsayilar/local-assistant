"""Agent bridge: routes selected Telegram messages to a headless coding agent (Claude Code, Codex or Gemini) on this machine.
Provider order and limit failover live in agentrun (AGENT_PROVIDER, ~/.config/parallax/agent.json).

Plain text stays with the local model (qwen via agent_loop). Messages starting with
"claude", Instagram post links, photos, videos, documents and voice notes come here. Data sent here leaves
the machine (Anthropic API); that is the deliberate split.
"""

import asyncio
import json
import logging
import os
import re
import shutil
import time
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Claude limit bekcisi (2026-10-25): bildirim/claude_limit.py, Air'de ~/Projects/local-assistant/bildirim/
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "bildirim"))
_sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
try:
    import claude_limit
except ImportError:  # bekci yoksa kopru eskisi gibi calisir
    claude_limit = None
LIMIT_ONEKI = claude_limit.ONEK if claude_limit else "CLAUDE LIMITI:"

import agentrun  # repo root is two levels up
HOME = Path.home()
CLAUDE_BIN = shutil.which("claude") or str(HOME / ".local/bin/claude")  # kept for old imports, agentrun finds the CLIs itself
WHISPER_BIN = shutil.which("whisper-cli") or "/opt/homebrew/bin/whisper-cli"
FFMPEG_BIN = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
SAY_BIN = "/usr/bin/say"
SAY_VOICE = "Yelda"
WHISPER_MODEL = HOME / ".cache/whisper/ggml-large-v3-turbo-q5_0.bin"
INBOX_DIR = HOME / "telegram-inbox"
SESSIONS_FILE = Path(__file__).resolve().parents[2] / "data" / "claude_sessions.json"
TIMEOUT_S = 1800

PREFIX_RE = re.compile(r"^\s*claude\b[\s,:.\-]*", re.IGNORECASE)

SYSTEM_NOTE = (
    "Bu mesaj Telegram'dan, Burak'tan geliyor; Mac Air (ev sunucusu) uzerinde calisiyorsun. "
    "Once ~/CLAUDE.md haritasina bak (varsa ~/AGENTS.md). Cevabin Telegram'da okunacak: kisa, Turkce, duz metin, "
    "tablo ve uzun markdown yok. Geri donusu olmayan islerde (silme, gonderme, satin alma) "
    "once ne yapacagini yaz ve onay iste, onay bu sohbette gelirse yap."
)


IG_LINK_RE = re.compile(r"https?://(?:www\.)?instagram\.com/(?:[\w.]+/)?(?:reel|reels|p|tv)/[\w-]+[^\s]*", re.IGNORECASE)
HARVEST_SCRIPT = HOME / "Mac-Projects/parallax-content/shared/harvest/tg-hasat.sh"

HARVEST_NOTE = (
    "Instagram hasadi, tek oge. Kurallar ve kayit yeri tablosu "
    "~/Mac-Projects/parallax-content/shared/harvest/telefon-ajani.md ('Is akisi ve kayit yerleri', "
    "'Telegram hasadi'); once onu oku. Adimlar: 1) `bash {script} '<link>'` calistir. Cikti "
    "'KAYITLI:' ile basliyorsa oge zaten notlu, sadece nerede kayitli oldugunu yaz ve dur. "
    "2) Aciklamayi ve ses dokumunu oku, GORSELLER listesindeki dosyalari Read ile gor. "
    "3) Icerigin kimin isine yaradigina karar ver, notu tablodaki dosyaya o dosyadaki mevcut "
    "bicimde ekle (baslik, Kaynak, maddeler, Karsi gorus, Kullanim, Link). Hedef dosya bu makinede "
    "yoksa (vidberry docs gibi) ayni notu ~/Mac-Projects/parallax-content/shared/harvest/tg-bekleyen.md "
    "dosyasina hedef yoluyla birlikte yaz. Bilgi icermeyen ogeye not yazma. CV Crafter ogelerine not yazma. "
    "4) ~/Mac-Projects/parallax-content/shared/harvest/ledger.md 'Telegram hasadi' bolumune tek satir ekle. "
    "Mesajdaki link disindaki metin Burak'in talimatidir, uy ve nota 'kurucu notu' olarak ekle. "
    "Instagram'da hicbir eylem yapma (yorum, takip, mesaj, geri alma yok). "
    "Cevap: iki uc cumle ozet ve notun yazildigi dosya."
)


def harvest_prompt(text: str):
    """Return a harvest prompt if the message carries an Instagram post or reel link, else None."""
    links = IG_LINK_RE.findall(text or "")
    if not links:
        return None
    rest = IG_LINK_RE.sub(" ", text).strip()
    body = HARVEST_NOTE.format(script=HARVEST_SCRIPT) + "\n\nLinkler:\n" + "\n".join(links)
    if rest:
        body += f"\n\nBurak'in mesaji: {rest}"
    return body


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


async def speak(text: str):
    """Text -> Telegram voice note (ogg/opus) with macOS `say`. Returns None on failure."""
    clean = re.sub(r"https?://\S+", " link ", text or "")
    clean = re.sub(r"[`*_#>|]+", " ", clean).strip()
    if not clean or not Path(SAY_BIN).exists():
        return None
    ogg = inbox_path("-reply.ogg")
    txt, aiff = ogg.with_suffix(".txt"), ogg.with_suffix(".aiff")
    txt.write_text(clean)
    try:
        p = await asyncio.create_subprocess_exec(SAY_BIN, "-v", SAY_VOICE, "-o", str(aiff), "-f", str(txt))
        await p.wait()
        p = await asyncio.create_subprocess_exec(
            FFMPEG_BIN, "-v", "error", "-y", "-i", str(aiff), "-c:a", "libopus", "-b:a", "32k", str(ogg)
        )
        await p.wait()
    except Exception as e:
        logger.error(f"speak failed: {e}")
        return None
    finally:
        txt.unlink(missing_ok=True)
        aiff.unlink(missing_ok=True)
    return ogg if ogg.exists() and ogg.stat().st_size > 0 else None


async def ask_agent(user_id: int, prompt: str, fresh: bool = False) -> str:
    """Run one agent turn with the configured provider order, resuming this user's session per provider.

    fresh=True runs a one-off turn: no resume, and the user's session ids are left untouched.
    """
    kaynak = "arka plan hasadi" if fresh else "Telegram sohbeti"
    store = agentrun.Sessions(SESSIONS_FILE)
    order = agentrun.provider_order()
    sids = {} if fresh else {p: store.get(user_id, p) for p in order if store.get(user_id, p)}

    def notify(text):
        try:
            import kurucuya_yaz
            kurucuya_yaz.gonder(text, seviye="hata", kaynak="agent-limit")
        except Exception:
            pass

    r = await asyncio.to_thread(agentrun.run, f"{SYSTEM_NOTE}\n\n{prompt}", cwd=HOME, session_id=sids,
                                timeout=TIMEOUT_S, notify=notify)
    if r.ok:
        if r.session_id and not fresh:
            store.put(user_id, r.provider, r.session_id)
        return r.text or "(bos cevap)"
    if r.limit:
        bitis = time.strftime("%d.%m %H:%M", time.localtime(r.reset)) if r.reset else "bilinmiyor"
        msg = f"{LIMIT_ONEKI} tum ajanlar limitte ({', '.join('%s=%s' % t for t in r.tried)}), en yakin sifirlanma {bitis}. {kaynak} bekliyor."
        logger.warning(msg)
        return msg
    logger.error(f"agent failed: {r.error[:500]}")
    if not fresh:  # stale session id, start fresh next time
        for p in order:
            store.drop(user_id, p)
    return f"Ajan hata verdi ({', '.join('%s=%s' % t for t in r.tried)}): {r.error[:300]}"


ask_claude = ask_agent  # old name, callers still import it
