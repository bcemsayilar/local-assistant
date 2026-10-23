# Local Assistant - TODO

## Aktif
- [ ] **Ay sonu finans guncellemesi (Ekim 2026):** kurucu kart ekstrelerini ve guncel yatirim detaylarini verecek, finance-tracker'a (Air) islenecek. Portfoyde artik hisse var: ~2026-10-15 para piyasasi fonundan 100k bozuldu (kurucu beyani: ~6k kesinti, buyuk ihtimalle getiri uzerinden stopaj, dekontla dogrulanacak), Gen Ilac (GENIL) 4.88 TL'den ~96k alindi, yani yaklasik 19.670 lot. Ekstre gelince alis dekontu, lot, maliyet ve fon bozma kesintisinin kalemi teyit edilsin; `baseline-analiz.md` fon bakiyesi (340k) bu cikisla guncellenmeli. Kurucu ortalama dusurme icin +50k dusunuyor, karar verilmedi
- [ ] **Anahtar yönetimini merkezileştir (kurucu 2026-10-24):** bugün herkes `~/Mac-Projects/vidberry/.env`'i kullanıyor çünkü en kapsamlısı o; anahtarlar bir app deposunun içinde, Air'de yok, her makineye elle kopyalanıyor (ASC `.p8`, ASA, ops anahtarı). Hedef: tek kanonik anahtar deposu (app'ten bağımsız, iki makinede aynı yolda, git dışı, 600), app `.env`'leri yalnız kendi anahtarlarını tutar, `service-access.md` bu depoya işaret eder. Ağır secret yöneticisi istenmiyor (kurucu 2026-10-04), basit çözüm
- [ ] **Merkezi kontrolör ajanı (kurucu fikri 2026-10-23, acele yok):** spend guard (Clear Wave ASA), Supabase keep-alive ve benzeri koruma ve ping işlerini tek merkezden yöneten, Remote Control ile uzaktan müdahale edilebilen statik bir kontrolör. Her yeni app için kaynak limitlerini (reklam bütçesi, Fal, OpenAI, Supabase, AWS) okuyup eşikte durduran tek kayıt ve tek zamanlayıcı. Bugünkü parçalar: `watercleaner/asa/spend_guard.py` (Air), `aws/supabase-keepalive` (Lambda), Air `air-orkestrator` (istek kutusu ve Remote Control oturumu `air-rc`). Kalıp `General App Guidlines/day-one-decisions.md` bölüm 7 "Spend guards are a standard component"
- [ ] **lifeOS projesi**: 2026-06-05 pivot, Cognee Mac Air'de surdurulebilir bulunmadi, yeni aday PewDiePie Odysseus. Detay: `projects/lifeOS/README.md` "STRATEJI PIVOT".

## PARKED
- [ ] Deco mesh'te ayri misafir WiFi, ziyaretciler LAN'a acik servislere ulasamasin. Deco uygulamasi ister, uzaktan yapilamiyor. Kararlar (FileVault kapali, statik IP ile port yonlendirme yok, Tailscale ACL) `home-server.md`'de.

## Arastirilacak
- [ ] Yazilimcilar icin "20B" vergi muafiyetini arastir (Turkiye, yazilimci/gelistirici gelir vergisi istisnasi, sartlar ve basvuru)
