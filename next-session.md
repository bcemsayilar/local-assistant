# Next Session - Devir Notu (güncel: 2026-11-10 gece)

Önce `~/.claude/CLAUDE.md`, sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md`, `agent-portability.md` ve `home-server.md`; servise dokunmadan önce `service-access.md`. Sistem şeması https://claude.ai/artifact/7RwAweEfyNQutzLT785WHY (kaynak `docs/sistem-semasi.html`). Açık işler yalnız `TODO.md`'de, denetim bulguları yalnız `docs/audit/ACIK-BULGULAR.md`'de; bu dosya yalnız devir notudur ve iş listesi tutmaz. Kurucu sparring partner ve KISA cevap ister; ürün adından ve altyapıdan varsayma, önce kontrol et; geri dönüşü olmayan işler ve commit önce onay; tarih ya da süre tahmini verme.

## Durum (2026-11-10 gece doğrulandı)

- **Bildirim modu `evde`** (Air `~/Projects/local-assistant/bildirim/mod`). Seviyeler `bilgi`, `hata`, `karar`, `engel`; `engel` modu ve nabzı yok sayar, her zaman Telegram'a gider (kural `session-organization.md` "Notification levels").
- **Telefonlar:** iki iPhone da Air'e bağlı ve WDA köprüleri çalışıyor (`com.parallax.wda-kopru-13`, `com.parallax.wda-kopru-pro`), WDA gözcüsü `com.parallax.wda-gozcu`. Kilit `kilit.py`, kural `telefon-ajani.md`.
- **Mağaza:** VidBerry 1.3.7 2026-11-09'da yayına girdi (vidberry oturumu henüz bilmiyor, sicil S-04). As Shot, Onscript (2026-10-28'den beri) ve Pillowtale (2026-11-04'ten beri) "Waiting for Review"; yeni uygulamaların yayın türü MANUAL. Gift Almanac, Beeward, Printmargin gönderim için kurucu kararında (TODO).
- **Bekleyen dış onaylar:** Meta App Review (yeniden başvuru 2026-11-04), TikTok Parallax Publisher (2026-11-01), YouTube API denetimi (2026-11-08); üçü de API'den okunmuyor, panelden bakılır.
- **Claude kredisi:** Anthropic relink onayı yok; 14 ve 16 Kasım işi TODO "Max aylık 100 dolar" maddesinde.
- **Bugün kapananlar (tekrar açma):** Air'deki VidBerry reel serisi 18 zamanlayıcıları kaldırıldı; `~/Mac-Projects` kökündeki eski ev klasörü kopyası ve SSH anahtarları silindi; vidberry stash'indeki sırlar temizlendi; Air `apple.env` silindi ve `secrets sync-air` onu göndermiyor; Lightsail `yoldalazim-backend` durduruldu (silme kararı sicil S-32); dört yeni uygulama deposu ve commit'siz bütün depolar commit'lenip push'landı. Air'de AWS yönetici ve Supabase service role anahtarlarının kalması kurucu kararı. `main`'e doğrudan commit şu an sorun değil (kurucu kararı).

## Kurucuya sorulacak (TODO dışı)

- Global GSD kurulumu kaldırılsın mı (`~/.claude/settings.json` durum çubuğu `gsd-statusline.js` ve `gsd-check-update.js` hook'u; kaldırılırsa yedeğe taşınır, durum çubuğu sade bir betikle değişir).
- 2026-11-04 devir notundan kalan, bu turda doğrulanmayan sorular: Mixpanel'de dev ve prod ayrı proje mi olsun; Clear Wave CTA kararı; Air Chrome profilinde Coinbase ve Chrome Remote Desktop ne olacak. Kurucu cevaplayınca ilgili dosyaya yazılır, buradan silinir.
- Hasat aracı açığı (self-branding'e iletilecek): `collect.py` benburakcem General kutusunda kaydırmıyor, `collect2.py` ve `collect3.py` var ama `telefon-ajani.md`'de yok (2026-11-10 grep).
