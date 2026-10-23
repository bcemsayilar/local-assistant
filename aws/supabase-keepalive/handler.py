"""supabase-keepalive: Supabase Free plandaki projeleri 7 gunluk hareketsizlik durdurmasina karsi canli tutar.
EventBridge 12 saatte bir cagirir; her projede herkese acik (publishable ya da anon) anahtarla tek satirlik bir REST okumasi yapar.
Sorgu RLS yuzunden bos ya da yetkisiz donse bile veritabanina ulasir, Supabase bunu aktivite sayar. 402 (kota kisiti) veritabanina ulasmaz.
Proje listesi PROJECTS ortam degiskeninde: [{"ref","key","path"}]. Gizli anahtar ya da hesap token'i yok."""
import json, os, urllib.request, urllib.error

def handler(event, context):
    out = []
    for p in json.loads(os.environ["PROJECTS"]):
        url = "https://%s.supabase.co/rest/v1/%s" % (p["ref"], p["path"])
        req = urllib.request.Request(url, headers={"apikey": p["key"], "Authorization": "Bearer " + p["key"]})
        try:
            with urllib.request.urlopen(req, timeout=20) as r: code, body = r.status, r.read(200).decode("utf-8", "replace")
        except urllib.error.HTTPError as e: code, body = e.code, e.read(200).decode("utf-8", "replace")
        except Exception as e: code, body = 0, repr(e)[:200]
        # 200, 401, 403, 404 veritabanina ulasti demek; 402 kota kisiti, 0 ag hatasi, 5xx proje kapali
        ok = code in (200, 206, 401, 403, 404)
        out.append({"ref": p["ref"], "code": code, "ok": ok, "body": body if not ok else ""})
    print(json.dumps(out))
    # 402 kota kisiti: bilinen durum, uyari degil. Baska her basarisizlik (ag hatasi, 5xx, durdurulmus proje) Lambda hatasi olur,
    # CloudWatch alarmi supabase-keepalive-hata SNS ile contact@parallaxtechnologies.net'e e-posta atar
    bad = [o for o in out if not o["ok"] and o["code"] != 402]
    if bad: raise RuntimeError("supabase erisilemiyor: " + json.dumps(bad))
    return out
