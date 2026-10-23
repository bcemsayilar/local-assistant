#!/usr/bin/python3
"""kosu.py : air-orkestrator kosucusu. LaunchAgent com.parallax.air-orkestrator 2 dakikada bir calistirir.
istek/ klasorunde yeni dosya varsa hepsini tek mesajda kalici orkestrator oturumuna (claude -p --resume) verir, cevaplarin yazildigini kontrol eder,
islenen istekleri islenen/<gun>/ altina tasir. Ayni anda tek kosu (kilit dosyasi). Kurallar CLAUDE.md'de."""
import datetime, json, os, shutil, subprocess, sys, time
H = os.path.expanduser("~"); D = os.path.join(H, "Projects/air-orkestrator")
IST, ISL, CEV, LOG = (os.path.join(D, x) for x in ("istek", "isleniyor", "cevap", "kosu.log"))
LOCK = os.path.join(D, "kosu.lock"); SID = os.path.join(D, "oturum.id"); CLAUDE = os.path.join(H, ".local/bin/claude")
TIMEOUT_S = 2700

def log(*a):
    with open(LOG, "a") as f: f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")

def token():
    for line in open(os.path.join(H, "Projects/local-assistant/.env")):
        if line.startswith("CLAUDE_CODE_OAUTH_TOKEN="): return line.split("=", 1)[1].strip().strip('"')
    return None

def main():
    for d in (IST, ISL, CEV): os.makedirs(d, exist_ok=True)
    if os.path.exists(LOCK):
        try:
            os.kill(int(open(LOCK).read().strip()), 0); return
        except (OSError, ValueError): os.remove(LOCK)
    yeni = sorted(f for f in os.listdir(IST) if f.endswith(".md"))
    eski = sorted(f for f in os.listdir(ISL) if f.endswith(".md"))  # yarida kalmis kosudan
    if not yeni and not eski: return
    open(LOCK, "w").write(str(os.getpid()))
    try:
        for f in yeni: shutil.move(os.path.join(IST, f), os.path.join(ISL, f))
        isler = sorted(f for f in os.listdir(ISL) if f.endswith(".md"))
        govde = "\n\n".join("### istek: %s\n%s" % (f, open(os.path.join(ISL, f)).read().strip()) for f in isler)
        prompt = ("Yeni istekler geldi (%d). CLAUDE.md'deki 'Her istek icin' adimlarini uygula, her biri icin cevap/<istek-adi> dosyasini yaz. "
                  "Bitince tek satir ozet ver.\n\n%s" % (len(isler), govde))
        env = dict(os.environ, CLAUDE_CODE_OAUTH_TOKEN=token() or "", PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:" + H + "/.local/bin")
        cmd = [CLAUDE, "-p", prompt, "--output-format", "json", "--dangerously-skip-permissions"]
        sid = open(SID).read().strip() if os.path.exists(SID) else None
        if sid: cmd += ["--resume", sid]
        log("kosu basladi", len(isler), "istek", "resume" if sid else "yeni oturum")
        p = None
        try:
            p = subprocess.run(cmd, cwd=D, env=env, capture_output=True, text=True, timeout=TIMEOUT_S)
            out = json.loads(p.stdout) if p.stdout.strip().startswith("{") else {}
        except subprocess.TimeoutExpired:
            out = {"result": "zaman asimi", "is_error": True}
        if out.get("session_id"): open(SID, "w").write(out["session_id"])
        if sid and not out.get("session_id"):  # bozuk oturum: bir sonraki kosu yeni oturumla baslasin, istekler isleniyor/ de kalir
            os.remove(SID); log("resume basarisiz, oturum sifirlandi", (p.stderr if p else "zaman asimi")[:300]); return
        gun = os.path.join(D, "islenen", datetime.date.today().isoformat()); os.makedirs(gun, exist_ok=True)
        for f in isler:
            c = os.path.join(CEV, f)
            if not os.path.exists(c):
                open(c, "w").write("DURUM: BELIRSIZ\nOrkestrator bu istek icin cevap dosyasi yazmadi. Kosu ozeti: %s\n" % str(out.get("result", ""))[:1500])
            shutil.move(os.path.join(ISL, f), os.path.join(gun, f))
        log("kosu bitti", str(out.get("result", ""))[:300].replace("\n", " "))
    finally:
        if os.path.exists(LOCK): os.remove(LOCK)

if __name__ == "__main__": main()
