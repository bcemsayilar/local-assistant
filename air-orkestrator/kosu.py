#!/usr/bin/python3
"""kosu.py : air-orkestrator kosucusu. LaunchAgent com.parallax.air-orkestrator 2 dakikada bir calistirir.
istek/ klasorunde yeni dosya varsa hepsini tek mesajda kalici orkestrator oturumuna (claude -p --resume) verir, cevaplarin yazildigini kontrol eder,
islenen istekleri islenen/<gun>/ altina tasir. Ayni anda tek kosu (kilit dosyasi). Kurallar CLAUDE.md'de."""
import datetime, json, os, selectors, shutil, subprocess, sys, time
H = os.path.expanduser("~"); D = os.path.join(H, "Projects/air-orkestrator")
IST, ISL, CEV, LOG = (os.path.join(D, x) for x in ("istek", "isleniyor", "cevap", "kosu.log"))
LOCK = os.path.join(D, "kosu.lock"); SID = os.path.join(D, "oturum.id"); CLAUDE = os.path.join(H, ".local/bin/claude")
TIMEOUT_S = 2700
# Bekci (2026-10-25): kosu ilk API cagrisinda cevapsiz takilabiliyor (uc kez 45 dk bosa gitti).
# stream-json her olayi satir satir verir; model beklenirken STALL_MODEL_S, arac calisirken STALL_TOOL_S
# (Bash araci en fazla 10 dk) boyunca yeni satir gelmezse surec oldurulur ve bir kez yeniden denenir.
STALL_MODEL_S, STALL_TOOL_S = 300, 660
# Claude limit bekcisi (2026-10-25): limit doluyken kosu Claude'u cagirmaz, istekler isleniyor/ da kalir ve limit bitince islenir
sys.path.insert(0, os.path.join(H, "Projects/local-assistant/bildirim"))
try: import claude_limit
except ImportError: claude_limit = None

def log(*a):
    with open(LOG, "a") as f: f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")

def token():
    for line in open(os.path.join(H, "Projects/local-assistant/.env")):
        if line.startswith("CLAUDE_CODE_OAUTH_TOKEN="): return line.split("=", 1)[1].strip().strip('"')
    return None

def calistir(cmd, env):
    """claude -p'yi stream-json ile calistirir. Donus: (sonuc olayi ya da {}, durum) ; durum 'tamam', 'takildi' ya da 'zaman asimi'."""
    p = subprocess.Popen(cmd, cwd=D, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    fd = p.stdout.fileno(); sel = selectors.DefaultSelector(); sel.register(fd, selectors.EVENT_READ)
    basla = son = time.time(); arac = False; sonuc = {}; tampon = b""; ham = []
    try:
        while True:
            if time.time() - basla > TIMEOUT_S: return sonuc, "zaman asimi"
            if time.time() - son > (STALL_TOOL_S if arac else STALL_MODEL_S): return sonuc, "takildi"
            if not sel.select(timeout=10): continue
            parca = os.read(fd, 65536)
            if not parca:
                p.wait()
                if claude_limit:
                    limitli, reset, metin = claude_limit.incele("\n".join(ham))
                    if limitli: return {"limit_reset": reset, "result": metin}, "limit"
                return sonuc, "tamam"
            son = time.time(); tampon += parca
            *satirlar, tampon = tampon.split(b"\n")
            for line in satirlar:
                if b"rate_limit_event" in line or b'"result"' in line: ham.append(line.decode(errors="replace"))
                try: d = json.loads(line)
                except ValueError: continue
                if d.get("type") == "result": sonuc = d
                elif d.get("type") == "assistant":
                    c = d.get("message", {}).get("content") or []
                    arac = any(isinstance(x, dict) and x.get("type") == "tool_use" for x in c)
                elif d.get("type") == "user": arac = False
    finally:
        if p.poll() is None: p.kill(); p.wait()

def main():
    for d in (IST, ISL, CEV): os.makedirs(d, exist_ok=True)
    if os.path.exists(LOCK):
        try:
            os.kill(int(open(LOCK).read().strip()), 0); return
        except (OSError, ValueError): os.remove(LOCK)
    yeni = sorted(f for f in os.listdir(IST) if f.endswith(".md"))
    eski = sorted(f for f in os.listdir(ISL) if f.endswith(".md"))  # yarida kalmis kosudan
    if not yeni and not eski: return
    if claude_limit and claude_limit.aktif()[0]:
        isaret = os.path.join(D, ".limit-loglandi")  # limit penceresi basina tek log satiri
        if not os.path.exists(isaret) or os.path.getmtime(isaret) < time.time() - 3600:
            log("claude limiti suruyor, %d istek bekliyor, sifirlanma %s" % (len(yeni) + len(eski), claude_limit.saat(claude_limit.aktif()[1])))
            open(isaret, "w").close()
        return
    open(LOCK, "w").write(str(os.getpid()))
    try:
        for f in yeni: shutil.move(os.path.join(IST, f), os.path.join(ISL, f))
        isler = sorted(f for f in os.listdir(ISL) if f.endswith(".md"))
        govde = "\n\n".join("### istek: %s\n%s" % (f, open(os.path.join(ISL, f)).read().strip()) for f in isler)
        prompt = ("Yeni istekler geldi (%d). CLAUDE.md'deki 'Her istek icin' adimlarini uygula, her biri icin cevap/<istek-adi> dosyasini yaz. "
                  "Bitince tek satir ozet ver.\n\n%s" % (len(isler), govde))
        env = dict(os.environ, CLAUDE_CODE_OAUTH_TOKEN=token() or "", PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:" + H + "/.local/bin")
        cmd = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose", "--dangerously-skip-permissions"]
        sid = open(SID).read().strip() if os.path.exists(SID) else None
        if sid: cmd += ["--resume", sid]
        log("kosu basladi", len(isler), "istek", "resume" if sid else "yeni oturum")
        out, durum = calistir(cmd, env)
        if durum == "takildi" and not out:  # bir kez yeniden dene
            log("kosu takildi, yeniden deneniyor"); out, durum = calistir(cmd, env)
        if durum == "limit":  # istekler isleniyor/ da kalir, cevap yazilmaz; limit bitince sonraki kosu isler
            msg = claude_limit.kaydet("air-orkestrator", out.get("result", ""), out.get("limit_reset", 0))
            log("kosu bitti CLAUDE LIMITI, istekler kuyrukta:", msg); return
        if durum != "tamam" and not out: out = {"result": durum, "is_error": True}
        if out.get("session_id"): open(SID, "w").write(out["session_id"])
        if sid and not out.get("session_id"):  # bozuk oturum: bir sonraki kosu yeni oturumla baslasin, istekler isleniyor/ de kalir
            os.remove(SID); log("resume basarisiz, oturum sifirlandi", durum); return
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
