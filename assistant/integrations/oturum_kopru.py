"""Telegram'dan belirli bir Air oturumuna kurucu mesaji (2026-10-24, teslim dogrulamasi 2026-10-25).

`af <mesaj>` ile baslayan metin, app-fabrikasi oturumunun tmux penceresine aynen yazilir ve Enter'a basilir.
Oturum bunu kullanici girdisi olarak gorur; baska bir oturumun aktardigi mesaj degildir. Bot yalniz
ALLOWED_USER_IDS'ten gelen mesaji isler, yani kaynak kurucunun Telegram hesabidir.

2026-10-25 dersi: oturum calisirken yazilan metin kayboldu (00:02 mesaji), bot yine "iletildi" demisti.
Artik oturum bosa dusene kadar beklenir, yazildiktan sonra giris satirinin bosaldigi dogrulanir.
"""

import asyncio
import re
import shutil
import subprocess

# onek -> tmux oturum adi
HEDEFLER = {"af": "app-fabrikasi"}
ONEK_RE = re.compile(r"^\s*(" + "|".join(HEDEFLER) + r")\b[\s:,.-]*", re.I)
TMUX = shutil.which("tmux") or "/opt/homebrew/bin/tmux"
MESGUL = "esc to interrupt"
BEKLEME_SN = 30 * 60


def route(text: str):
    """Onekli mesajsa (hedef, govde), degilse None."""
    m = ONEK_RE.match(text or "")
    if not m:
        return None
    return HEDEFLER[m.group(1).lower()], text[m.end():].strip()


def _ekran(hedef: str) -> str:
    return subprocess.run([TMUX, "capture-pane", "-pt", hedef], capture_output=True, text=True).stdout


def _giris_satiri(ekran: str) -> str:
    """Claude Code giris kutusundaki metin ('❯ ' ile baslayan son satir)."""
    satirlar = [l for l in ekran.splitlines() if l.lstrip().startswith("❯")]
    return satirlar[-1].lstrip()[1:].strip() if satirlar else ""


def _mesgul(ekran: str) -> bool:
    return MESGUL in "\n".join(ekran.splitlines()[-6:])


async def gonder(hedef: str, govde: str) -> str:
    """Oturum bosa dusunce yazar ve teslimi dogrular; kullaniciya gidecek sonucu doner."""
    if not govde:
        return "Bos mesaj, gonderilmedi."
    if subprocess.run([TMUX, "has-session", "-t", hedef], capture_output=True).returncode:
        return f"{hedef} oturumu acik degil (tmux). Mesaj gonderilmedi."
    satir = "[Kurucu, Telegram'dan] " + " / ".join(l.strip() for l in govde.splitlines() if l.strip())
    beklendi = 0
    while _mesgul(_ekran(hedef)) or _giris_satiri(_ekran(hedef)):
        if beklendi >= BEKLEME_SN:
            return f"{hedef} {BEKLEME_SN // 60} dakikadir mesgul ya da giris kutusu dolu. Mesaj GONDERILMEDI, tekrar dene."
        await asyncio.sleep(10)
        beklendi += 10
    subprocess.run([TMUX, "send-keys", "-t", hedef, "-l", satir], capture_output=True)
    await asyncio.sleep(1)
    subprocess.run([TMUX, "send-keys", "-t", hedef, "Enter"], capture_output=True)
    for _ in range(6):
        await asyncio.sleep(2)
        ekran = _ekran(hedef)
        if not _giris_satiri(ekran) and (_mesgul(ekran) or satir[:40] in ekran):
            return f"{hedef} oturumuna teslim edildi" + (f" ({beklendi // 60} dk bekledi)." if beklendi >= 60 else ".")
    return f"{hedef}: metin yazildi ama teslim dogrulanamadi. Giris kutusuna bak ya da tekrar gonder."
