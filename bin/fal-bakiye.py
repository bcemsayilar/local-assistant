#!/usr/bin/python3
"""fal-bakiye.py : Fal on odemeli bakiyesini okur, esigin altindaysa kurucuya 'engel' seviyesinde haber verir.

Neden: VidBerry'nin butun uretimi Fal bakiyesine bagli, bakiye biterse uretim durur (2026-11-19'da 11,67 USD'ye inmisti).
Calisma: Air'de gunde bir (zamanlama air-orkestrator'da), anahtar kasadan:
    ~/Projects/local-assistant/bin/secrets run fal -- python3 ~/Projects/local-assistant/bin/fal-bakiye.py
Esik FAL_BAKIYE_ESIK ile degisir (varsayilan 5 USD). Okuma basarisizsa 'hata' seviyesinde kaydedilir.
--kuru: bildirimi gondermez, yalniz ne yapacagini yazar (test icin).
"""
import json, os, sys, urllib.request

ESIK = float(os.environ.get("FAL_BAKIYE_ESIK", "5"))
KURU = "--kuru" in sys.argv


def bildir(metin, seviye):
    if KURU:
        print("KURU [%s] %s" % (seviye, metin)); return
    sys.path.insert(0, os.path.expanduser("~/Projects/local-assistant/bildirim"))
    try:
        import kurucuya_yaz
        kurucuya_yaz.gonder(metin, seviye=seviye, kaynak="fal-bakiye")
    except Exception as e:
        print("BILDIRIM KAPISI YOK: %s" % e)


def main():
    anahtar = os.environ.get("FAL_API_ADMIN_KEY")
    if not anahtar:
        bildir("Fal bakiyesi okunamadi: FAL_API_ADMIN_KEY ortamda yok.", "hata"); return 1
    try:
        r = urllib.request.Request("https://api.fal.ai/v1/account/billing?expand=credits",
                                   headers={"Authorization": "Key " + anahtar})
        d = json.load(urllib.request.urlopen(r, timeout=30))
        bakiye = float(d["credits"]["current_balance"])
    except Exception as e:
        bildir("Fal bakiyesi okunamadi: %s" % type(e).__name__, "hata"); return 1
    print("fal bakiye %.2f USD, esik %.2f" % (bakiye, ESIK))
    if bakiye < ESIK:
        bildir("Fal bakiyesi %.2f USD, esik %.2f USD. Biterse VidBerry uretimi durur. Yukleme: fal.ai/dashboard/billing" % (bakiye, ESIK), "engel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
