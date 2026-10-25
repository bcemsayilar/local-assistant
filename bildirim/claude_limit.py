#!/usr/bin/python3
"""claude_limit.py : Air'de Claude'u otomatik cagiran her isin ortak limit bekcisi (kurucu istegi 2026-10-25).

Claude Code abonelik limiti (5 saatlik ya da haftalik) dolunca `claude -p` hata ile doner. Bu modul o hatayi tanir,
sifirlanma zamaniyla birlikte claude-limit.json'a yazar, kurucuya bildirim kapisindan pencere basina bir kez "hata"
gecer ve diger islere "simdi cagirma, su saate kadar bekle" der. Boylece is kaybolmaz (cagiran isi kuyrukta birakir),
dongu donmez ve log okunur kalir.

Tanima iki yoldan: stream-json ciktisindaki rate_limit_event (status "rejected", resetsAt saniye) en kesin olani;
json ciktisinda yalniz metin vardir, o zaman LIMIT_RE ile bakilir ve sifirlanma bilinmiyorsa VARSAYILAN_BEKLEME kadar beklenir.
"""
import json, os, re, sys, time

D = os.path.dirname(os.path.abspath(__file__))
DURUM = os.path.join(D, "claude-limit.json")
VARSAYILAN_BEKLEME = 1800
ONEK = "CLAUDE LIMITI:"  # cagiranlara donen metnin basi; bu onekle baslayan cevap is sonucu degildir
LIMIT_RE = re.compile(r"usage (credit )?limit reached|hit your (usage |session |weekly )?limit|limit reached|out of extra usage"
                      r"|rate[ _-]?limit|overloaded|\b429\b|\b529\b|credit balance too low", re.I)


def _yaz(d):
    tmp = DURUM + ".tmp"; json.dump(d, open(tmp, "w"), ensure_ascii=False); os.replace(tmp, DURUM)


def aktif():
    """(limit suruyor mu, bitis epoch, mesaj)."""
    try: d = json.load(open(DURUM))
    except (OSError, ValueError): return False, 0, ""
    return time.time() < d.get("bitis", 0), d.get("bitis", 0), d.get("mesaj", "")


def saat(epoch):
    return time.strftime("%d.%m %H:%M", time.localtime(epoch)) if epoch else "bilinmiyor"


def incele(stdout):
    """claude -p ciktisini (json ya da stream-json) okur. Donus: (limitli mi, resetsAt ya da 0, sonuc metni)."""
    sonuc, reddedildi, reset, hata, json_var = "", False, 0, False, False
    for satir in (stdout or "").splitlines() or [""]:
        try: d = json.loads(satir)
        except ValueError: continue
        json_var = True
        if d.get("type") == "rate_limit_event":
            i = d.get("rate_limit_info") or {}
            if i.get("status") == "rejected": reddedildi, reset = True, int(i.get("resetsAt") or 0)
        elif d.get("type") == "result" or "result" in d:
            sonuc, hata = str(d.get("result") or ""), bool(d.get("is_error"))
    if not json_var: sonuc, hata = (stdout or "")[-500:], True  # json yok: CLI hata metni basmis
    # Normal bir cevap Instagram'in 429'undan soz edebilir; metne yalniz hata sonucunda bakilir
    limitli = reddedildi or (hata and bool(LIMIT_RE.search(sonuc)))
    if limitli and not reset:
        m = re.search(r"\|(\d{10})\b", sonuc)  # eski bicim: "Claude AI usage limit reached|1793120400"
        reset = int(m.group(1)) if m else 0
    return limitli, reset, sonuc


def kaydet(kaynak, mesaj, reset=0):
    """Limiti kaydeder, yeni bir pencereyse kurucuya bildirim kapisindan bir kez yazar. Donus: cagirana verilecek metin."""
    bitis = reset or int(time.time()) + VARSAYILAN_BEKLEME
    try:
        eski = json.load(open(DURUM)) if os.path.exists(DURUM) else {}
    except ValueError:
        eski = {}
    yeni_pencere = time.time() >= eski.get("bitis", 0)
    _yaz({"bitis": bitis, "kaynak": kaynak, "mesaj": mesaj[:300], "zaman": time.strftime("%Y-%m-%d %H:%M:%S"),
          "bitis_bilinen": bool(reset)})
    metin = "%s Claude kullanim limiti doldu (%s), sifirlanma %s%s. Is kuyrukta kaldi, sonra yeniden denenecek." % (
        ONEK, kaynak, saat(bitis), "" if reset else " (tahmini)")
    if yeni_pencere:
        try:
            sys.path.insert(0, D); import kurucuya_yaz
            kurucuya_yaz.gonder(metin + " Claude cevabi: " + mesaj[:200], seviye="hata", kaynak="claude-limit")
        except Exception:
            pass
    return metin


def bekle_metni(kaynak):
    """Limit suruyorsa cagirmadan donulecek metin, surmuyorsa None."""
    a, bitis, _ = aktif()
    return "%s limit suruyor, sifirlanma %s; %s Claude'u cagirmadi." % (ONEK, saat(bitis), kaynak) if a else None


if __name__ == "__main__":
    a, bitis, m = aktif()
    print("limit suruyor, bitis %s: %s" % (saat(bitis), m) if a else "limit yok")
