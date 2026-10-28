#!/usr/bin/python3
"""kosu.py : air-orkestrator kosucusu. LaunchAgent com.parallax.air-orkestrator 2 dakikada bir calistirir.
istek/ klasorunde yeni dosya varsa hepsini tek mesajda kalici orkestrator oturumuna (headless agent, resume) verir, cevaplarin yazildigini kontrol eder,
islenen istekleri islenen/<gun>/ altina tasir. Ayni anda tek kosu (kilit dosyasi). Kurallar CLAUDE.md'de."""
import datetime, json, os, selectors, shutil, subprocess, sys, time
H = os.path.expanduser("~"); D = os.path.join(H, "Projects/air-orkestrator")
IST, ISL, CEV, LOG = (os.path.join(D, x) for x in ("istek", "isleniyor", "cevap", "kosu.log"))
LOCK = os.path.join(D, "kosu.lock"); SID = os.path.join(D, "oturum.id"); SIDS = os.path.join(D, "oturum.json")
TIMEOUT_S = 2700
# Bekci (2026-10-25): kosu ilk API cagrisinda cevapsiz takilabiliyor (uc kez 45 dk bosa gitti).
# stream-json her olayi satir satir verir; model beklenirken STALL_MODEL_S, arac calisirken STALL_TOOL_S
# (Bash araci en fazla 10 dk) boyunca yeni satir gelmezse surec oldurulur ve bir kez yeniden denenir.
STALL_MODEL_S, STALL_TOOL_S = 300, 660
# Saglayici bagimsiz calistirici (2026-10-28): agentrun Claude, Codex ve Gemini arasinda limit gecisini yapar;
# limitteki saglayici sifirlanana kadar atlanir, hepsi limitteyse istekler isleniyor/ da kalir ve sonraki kosu isler.
sys.path.insert(0, os.path.join(H, "Projects/local-assistant")); sys.path.insert(0, os.path.join(H, "Mac-Projects/local-assistant"))
import agentrun

def log(*a):
    with open(LOG, "a") as f: f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")

def main():
    for d in (IST, ISL, CEV): os.makedirs(d, exist_ok=True)
    if os.path.exists(LOCK):
        try:
            os.kill(int(open(LOCK).read().strip()), 0); return
        except (OSError, ValueError): os.remove(LOCK)
    yeni = sorted(f for f in os.listdir(IST) if f.endswith(".md"))
    eski = sorted(f for f in os.listdir(ISL) if f.endswith(".md"))  # yarida kalmis kosudan
    if not yeni and not eski: return
    order = agentrun.provider_order()
    if all(agentrun.parked_until(p) or not agentrun.core.find_bin(p) for p in order):
        isaret = os.path.join(D, ".limit-loglandi")  # limit penceresi basina tek log satiri
        if not os.path.exists(isaret) or os.path.getmtime(isaret) < time.time() - 3600:
            bitis = min([agentrun.parked_until(p) for p in order if agentrun.parked_until(p)] or [0])
            log("tum ajanlar limitte ya da kurulu degil, %d istek bekliyor, en yakin sifirlanma %s" % (len(yeni) + len(eski), time.strftime("%d.%m %H:%M", time.localtime(bitis)) if bitis else "bilinmiyor"))
            open(isaret, "w").close()
        return
    open(LOCK, "w").write(str(os.getpid()))
    try:
        for f in yeni: shutil.move(os.path.join(IST, f), os.path.join(ISL, f))
        isler = sorted(f for f in os.listdir(ISL) if f.endswith(".md"))
        govde = "\n\n".join("### istek: %s\n%s" % (f, open(os.path.join(ISL, f)).read().strip()) for f in isler)
        prompt = ("Yeni istekler geldi (%d). talimat dosyasindaki (CLAUDE.md ya da AGENTS.md) 'Her istek icin' adimlarini uygula, her biri icin cevap/<istek-adi> dosyasini yaz. "
                  "Bitince tek satir ozet ver.\n\n%s" % (len(isler), govde))
        store = agentrun.Sessions(SIDS)
        if os.path.exists(SID) and not os.path.exists(SIDS):  # eski tek dosya: Claude oturumu
            store.put("orkestrator", "claude", open(SID).read().strip())
        sids = {p: store.get("orkestrator", p) for p in order if store.get("orkestrator", p)}
        log("kosu basladi", len(isler), "istek", "resume" if sids else "yeni oturum", ">".join(order))
        kw = dict(cwd=D, session_id=sids, timeout=TIMEOUT_S, idle_s=STALL_MODEL_S, idle_tool_s=STALL_TOOL_S)
        r = agentrun.run(prompt, **kw)
        if "idle" in (r.error or "") and not r.limit:  # bir kez yeniden dene
            log("kosu takildi, yeniden deneniyor"); r = agentrun.run(prompt, **kw)
        if r.limit:  # istekler isleniyor/ da kalir, cevap yazilmaz; limit bitince sonraki kosu isler
            log("kosu bitti AJAN LIMITI, istekler kuyrukta:", ", ".join("%s=%s" % t for t in r.tried), (r.error or "")[:200]); return
        out = {"result": r.text if r.ok else (r.error or "hata"), "is_error": not r.ok, "session_id": r.session_id if r.ok else ""}
        if r.ok and r.session_id: store.put("orkestrator", r.provider, r.session_id)
        if sids and not r.ok:  # bozuk oturum: bir sonraki kosu yeni oturumla baslasin, istekler isleniyor/ de kalir
            for p in order: store.drop("orkestrator", p)
            log("resume basarisiz, oturum sifirlandi", ", ".join("%s=%s" % t for t in r.tried), (r.error or "")[:200]); return
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
