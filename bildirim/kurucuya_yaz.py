#!/usr/bin/python3
"""kurucuya_yaz.py : Air'den kurucuya giden her Telegram bildiriminin tek kapisi.

Kural (kurucu karari 2026-10-25): kurucu Telegram'i gunluk kullanmiyor. Bilgi, rapor ve "su kadar is yapildi" mesajlari
Telegram'a gitmez, yalniz olay kaydina yazilir. Telegram'a giden tek sey "hata" ya da "karar" seviyesi ve ancak su iki
durumda: kurucu "to go" modunu actiysa (mod dosyasinda "to-go"), ya da Mac Pro'daki yonetim oturumlari (local-assistant,
self-branding) ulasilamazsa (nabiz.json bayat ya da iki oturum da kapali). Gerisini Mac Pro oturumlari olay kaydindan okur.
Kurucunun kendi yazdigi mesaja verilen cevap (Claude kopru, "af" komutlari) bu kapidan gecmez, onlar dogrudan cevaptir.

Kullanim, Python'dan:
    sys.path.insert(0, os.path.expanduser("~/Projects/local-assistant/bildirim")); import kurucuya_yaz
    kurucuya_yaz.gonder("metin", seviye="hata", kaynak="spend-guard")
Komut satirindan:  kurucuya_yaz.py <bilgi|hata|karar> <kaynak> [metin]   (metin yoksa stdin)
Mod:               kurucuya_yaz.py mod [evde|to-go]
"""
import json, os, sys, time, urllib.parse, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
ENV = os.path.join(os.path.dirname(D), ".env")
MOD, NABIZ, OLAY = (os.path.join(D, x) for x in ("mod", "nabiz.json", "olaylar.jsonl"))
NABIZ_BAYAT_S = 600  # Mac Pro nabzi 2 dakikada bir gelir; 10 dakika gelmezse Mac Pro ulasilamaz sayilir
YONETIM = ("local-assistant", "self-branding")
ONEMLI = ("hata", "karar")


def mod():
    try: return open(MOD).read().strip() or "evde"
    except OSError: return "evde"


def pro_aktif():
    """Mac Pro'dan gelen son nabiz taze mi ve icinde en az bir yonetim oturumu acik mi."""
    try: n = json.load(open(NABIZ))
    except (OSError, ValueError): return False
    return time.time() - n.get("zaman", 0) < NABIZ_BAYAT_S and any(o in n.get("oturumlar", []) for o in YONETIM)


def _telegram(metin):
    e = {}
    for l in open(ENV, encoding="utf-8"):
        if "=" in l and not l.strip().startswith("#"):
            k, v = l.strip().split("=", 1); e[k] = v.strip().strip('"').strip("'")
    tok, chat = e.get("TELEGRAM_BOT_TOKEN"), (e.get("ALLOWED_USER_IDS") or "").split(",")[0].strip()
    if not tok or not chat: return False
    try:
        for i in range(0, len(metin), 4000):
            d = urllib.parse.urlencode({"chat_id": chat, "text": metin[i:i + 4000], "disable_web_page_preview": "true"}).encode()
            urllib.request.urlopen("https://api.telegram.org/bot%s/sendMessage" % tok, d, timeout=20).read()
        return True
    except Exception:
        return False


def gonder(metin, seviye="bilgi", kaynak="?"):
    """Olayi kaydeder; kurala gore gerekiyorsa Telegram'a da yollar. Hicbir zaman istisna firlatmaz. Donus: Telegram'a gitti mi."""
    try:
        m = mod()
        if seviye not in ONEMLI: git, sebep = False, "bilgi seviyesi"
        elif m == "to-go": git, sebep = True, "to-go modu"
        elif not pro_aktif(): git, sebep = True, "Mac Pro yonetim oturumlari ulasilamaz"
        else: git, sebep = False, "evde, Mac Pro aktif"
        gitti = _telegram("[%s] %s" % (kaynak, metin)) if git else False
        with open(OLAY, "a") as f:
            f.write(json.dumps({"zaman": time.strftime("%Y-%m-%d %H:%M:%S"), "kaynak": kaynak, "seviye": seviye, "mod": m,
                                "telegram": gitti, "sebep": sebep, "metin": metin[:2000]}, ensure_ascii=False) + "\n")
        return gitti
    except Exception as x:
        print("kurucuya_yaz hatasi:", type(x).__name__, metin[:200])
        return False


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "mod":
        if len(a) > 1:
            if a[1] not in ("evde", "to-go"): sys.exit("mod evde ya da to-go olur")
            open(MOD, "w").write(a[1] + "\n")
        print(mod(), "| Mac Pro aktif" if pro_aktif() else "| Mac Pro ulasilamaz")
    elif len(a) >= 2 and a[0] in ("bilgi",) + ONEMLI:
        print("telegram" if gonder(" ".join(a[2:]) or sys.stdin.read().strip(), a[0], a[1]) else "kayit")
    else:
        sys.exit(__doc__)
