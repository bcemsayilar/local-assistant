"""Telegram'dan belirli bir Air oturumuna kurucu mesaji (2026-10-24).

`af <mesaj>` ile baslayan metin, app-fabrikasi oturumunun tmux penceresine aynen yazilir ve Enter'a basilir.
Oturum bunu kullanici girdisi olarak gorur; baska bir oturumun aktardigi mesaj degildir. Bot yalniz
ALLOWED_USER_IDS'ten gelen mesaji isler, yani kaynak kurucunun Telegram hesabidir.
"""

import re
import shutil
import subprocess

# onek -> tmux oturum adi
HEDEFLER = {"af": "app-fabrikasi"}
ONEK_RE = re.compile(r"^\s*(" + "|".join(HEDEFLER) + r")\b[\s:,.-]*", re.I)
TMUX = shutil.which("tmux") or "/opt/homebrew/bin/tmux"


def route(text: str):
    """Onekli mesajsa (hedef, govde), degilse None."""
    m = ONEK_RE.match(text or "")
    if not m:
        return None
    return HEDEFLER[m.group(1).lower()], text[m.end():].strip()


def gonder(hedef: str, govde: str) -> str:
    """Mesaji tmux penceresine yazar; kullaniciya gidecek kisa sonucu doner."""
    if not govde:
        return "Bos mesaj, gonderilmedi."
    if subprocess.run([TMUX, "has-session", "-t", hedef], capture_output=True).returncode:
        return f"{hedef} oturumu acik degil (tmux). Mesaj gonderilmedi."
    # Claude Code girisinde satir sonu mesaji erken gonderir; tek satira indir
    satir = "[Kurucu, Telegram'dan] " + " / ".join(l.strip() for l in govde.splitlines() if l.strip())
    r1 = subprocess.run([TMUX, "send-keys", "-t", hedef, "-l", satir], capture_output=True)
    r2 = subprocess.run([TMUX, "send-keys", "-t", hedef, "Enter"], capture_output=True)
    if r1.returncode or r2.returncode:
        return f"{hedef} penceresine yazilamadi."
    return f"{hedef} oturumuna iletildi."
