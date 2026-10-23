# Local Assistant - TODO

## Aktif
- [ ] n8n Twitter Bookmarks workflow'u `qwen3:4b` kullaniyor, model Air'de yok; bookmarks.json 2026-02-28'den beri guncellenmedi. Ya modeli guncelle ve beslemeyi kur ya workflow'u kapat
- [ ] **cemsayilar.com kisisel/proje sitesi** - projelerin + deneyim oldugu guzel bir sayfa (demirbulbuloglu.com tarzi: tek sayfa, koyu tema, isim+meslek hero, kisa bio, proje/deneyim listesi). Kok domain = cemsayilar.com (blog alt alanda: blog.cemsayilar.com). Cloudflare Pages ile static deploy; DNS'i Squarespace'ten Cloudflare'e tasi (o zaman blog CNAME + site kayitlari CLI'dan yonetilir). Template: Astro temasi (astro.build/themes) ya da hazir portfolio.
- [ ] **Ay sonu finans guncellemesi (Ekim 2026):** kurucu kart ekstrelerini ve guncel yatirim detaylarini verecek, finance-tracker'a (Air) islenecek. Portfoyde artik hisse var: ~2026-10-15 para piyasasi fonundan 100k bozuldu (kurucu beyani: ~6k kesinti, buyuk ihtimalle getiri uzerinden stopaj, dekontla dogrulanacak), Gen Ilac (GENIL) 4.88 TL'den ~96k alindi, yani yaklasik 19.670 lot. Ekstre gelince alis dekontu, lot, maliyet ve fon bozma kesintisinin kalemi teyit edilsin; `baseline-analiz.md` fon bakiyesi (340k) bu cikisla guncellenmeli. Kurucu ortalama dusurme icin +50k dusunuyor, karar verilmedi
- [ ] **Merkezi kontrolör ajanı (kurucu fikri 2026-10-23, acele yok):** spend guard (Clear Wave ASA), Supabase keep-alive ve benzeri koruma ve ping işlerini tek merkezden yöneten, Remote Control ile uzaktan müdahale edilebilen statik bir kontrolör. Her yeni app için kaynak limitlerini (reklam bütçesi, Fal, OpenAI, Supabase, AWS) okuyup eşikte durduran tek kayıt ve tek zamanlayıcı. Bugünkü parçalar: `watercleaner/asa/spend_guard.py` (Air), `aws/supabase-keepalive` (Lambda), Air `air-orkestrator` (istek kutusu ve Remote Control oturumu `air-rc`). Kalıp `General App Guidlines/day-one-decisions.md` bölüm 7 "Spend guards are a standard component"
- [ ] **lifeOS projesi**: 2026-06-05 pivot, Cognee Mac Air'de surdurulebilir bulunmadi, yeni aday PewDiePie Odysseus. Detay: `projects/lifeOS/README.md` "STRATEJI PIVOT".

## PARKED: Mac Air Hardening (watercleaner-7a denetimi, 2026-09-09)
PARKED 2026-10-09 (kurucu karari): kalan iki is uzaktan yapilamiyor, Tailscale ACL ve SSH admin konsolu oturumu, misafir WiFi Deco uygulamasi istiyor. Log rotation 2026-10-04'te kuruldu (`/etc/newsyslog.d/local-assistant.conf`).
Mac Air sunucusunun genel bilgisi (erişim, servisler, güvenlik): `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md`

Denetimde olculen durum: FileVault kapali, auto-login acik (elifberraksayilar), firewall acik, ekran kilidi okunamadi (macOS 26, System Settings'ten bakilacak). Tum arayuzlerde dinleyen portlar: 22 (ssh), 8000 (finance-agent), 22000 (syncthing), 3031, 8790. 2026-10-02 tekrar olcum: 3031 artik dinlemiyor; 8000 ve 8790 hala `*`, 8686 (finance-tracker) sadece Tailscale IP'sinde. Sadece localhost (dogru): 5678 (n8n), 11434 (ollama), 8585 (graphthulhu). Not: ASA spend guard bu denetimde kuruldu, calisiyor (launchd net.parallaxtechnologies.clearwave.spendguard, 4 saatte bir, ~/Projects/watercleaner).

- [x] FileVault: kullanici karari 2026-10-04, ACILMAYACAK (auto-login ve 7/24 otonom reboot oncelikli).
- [ ] Air icin Tailscale ACL + tag, ve Tailscale SSH'i ac (bugun kapali, advertised SSH host key yok). Erisim kontrolu tek yerde merkezi olarak iptal edilebilir hale gelir, makinelere dagilmis authorized_keys'e bagli kalmaz.
- [ ] Deco mesh'te ayri misafir WiFi, ziyaretciler LAN'a acik servislere ulasamasin.
- [ ] YAPMA (acikca): Superonline statik IP ile Deco'dan Air'e SSH ya da baska port-forward. Air zaten Tailscale ile her yerden, hucresel agdan, baska ulkeden erisilebilir, statik IP ek erisim getirmez, port-forward makinenin SSH'ini internetteki her tarayicinin onune koyar. Statik IP sadece Tailscale'in relay yerine direkt yol secmesine yarar (hiz meselesi). Gercekten public inbound gerekirse (ucuncu partiden n8n webhook gibi) dogru arac Cloudflare Tunnel ya da Tailscale Funnel, tek HTTPS yolu acar, router portu acmaz.
- [x] Plaintext secret'lar ve ajan zincirinin duz dosyadaki kilit anahtari (`~/.config/ajan/kc`): FileVault kapali kaldigi icin KABUL EDILMIS RISK (kurucu 2026-10-23).

## Claude kopru (Telegram)
- [ ] `relay.py` yalniz Air'de duruyor (Mac Pro'dan Air'deki Claude oturumuna mesaj gecip cevabi Telegram'a yollar); kullaniliyorsa repoya al, kullanilmiyorsa sil

## Arastirilacak
- [ ] Yazilimcilar icin "20B" vergi muafiyetini arastir (Turkiye, yazilimci/gelistirici gelir vergisi istisnasi, sartlar ve basvuru)
- [ ] fieldtheory CLI olgunlasinca n8n Twitter bookmarks workflow'una entegre et

## Tamamlanan (Son)
- [x] 2026-10-04: Telegram Claude kopru modu (claude prefix, gorsel, video, dosya, sesli not -> Air'deki Claude), whisper Air'e kuruldu, httpx token loglamasi kapatildi, Claude ve bot token'lari yenilendi
- [x] 2026-10-04: finance-agent PARKED, Air'de servisleri durduruldu (8000 artik dinlemiyor), 8790 pillowtale tarafindan localhost'a cekildi
- [x] Mac Air Tailscale erisimi kalici cozuldu (2026-09-04) - key expiry DISABLED (admin console), Tailscale.app login item eklendi, kirik/orphan homebrew.mxcl.tailscale LaunchAgent silindi, CLI integration acildi (SSH'tan `tailscale` komutu var: /usr/local/bin/tailscale), reusable auth key `~/.config/tailscale/authkey` (chmod 600). Break-glass re-auth: `tailscale up --authkey=$(cat ~/.config/tailscale/authkey)`. GUI artik loop'ta degil.
- [x] newsletter-project 3-akisli sistem kuruldu (2026-08-19) - LinkedIn (Baki) + PEAKUP AI Spotlight (liste) + Substack (Dunya Halleri), OpenAI gpt-5.4, Gmail kaynak (AI News + AlphaSignal), tarih-isimli klasor yapisi, og:image gorsel cekme, Turkce karakter + sober ton kurallari
- [x] Gmail MCP baglandi (read scope) - newsletter veri kaynagi icin
- [x] Ruya notu algilama bug fix (prefix-only)
- [x] Auto-delete misfire_grace_time duzeltme (24 saat)
- [x] Mac Air hibernate/sleep sorunlari cozumu
- [x] Ollama KV cache compression (q8_0)
- [x] Nemotron-mini denemesi (basarisiz, silindi)
- [x] Finance tracker 21 yeni islem eklendi
- [x] Data House dosya organizasyonu (tips/opensource/ideas bolundu)
- [x] fieldtheory kurulumu + 747 bookmark sync
- [x] RTK kurulumu
- [x] Development log guncellendi
