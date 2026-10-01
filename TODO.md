# Local Assistant - TODO

## Aktif
- [ ] Log rotation - bot-stdout.log ve bot-stderr.log icin newsyslog.d conf olustur
- [ ] Multimodal Asistan Faz 2 - Video destegi (ffmpeg), spor/ruya/gunluk sorgulama (RAG), sohbet modu
- [ ] Alibaba Coding Plan degerlendirmesi ($3-5/ay, qwen3.5, kimi k2.5, glm 5)
- [ ] **cemsayilar.com kisisel/proje sitesi** - projelerin + deneyim oldugu guzel bir sayfa (demirbulbuloglu.com tarzi: tek sayfa, koyu tema, isim+meslek hero, kisa bio, proje/deneyim listesi). Kok domain = cemsayilar.com (blog alt alanda: blog.cemsayilar.com). Cloudflare Pages ile static deploy; DNS'i Squarespace'ten Cloudflare'e tasi (o zaman blog CNAME + site kayitlari CLI'dan yonetilir). Template: Astro temasi (astro.build/themes) ya da hazir portfolio.
- [ ] **lifeOS projesi** — Kapsamli arastirma: Cognee, Mem0, Letta, Zep self-hosted seceneklerini karsilastir. Mevcut local-assistant ustune temporal/contradiction/unified ingestion katmani ekle. Detay: `projects/lifeOS/README.md`. Acik proje #2 (paralel: LinkedIn newsletter).

## Mac Air Hardening (watercleaner-7a denetimi, 2026-09-09)
Mac Air sunucusunun genel bilgisi (erişim, servisler, güvenlik): `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md`

Denetimde olculen durum: FileVault kapali, auto-login acik (elifberraksayilar), firewall acik, ekran kilidi okunamadi (macOS 26, System Settings'ten bakilacak). Tum arayuzlerde dinleyen portlar: 22 (ssh), 8000 (finance-agent), 22000 (syncthing), 3031, 8790. Sadece localhost (dogru): 5678 (n8n), 11434 (ollama), 8585 (graphthulhu). Not: ASA spend guard bu denetimde kuruldu, calisiyor (launchd net.parallaxtechnologies.clearwave.spendguard, 4 saatte bir, ~/Projects/watercleaner).

- [ ] finance-agent (8000) portunu 0.0.0.0 yerine 127.0.0.1'e bagla. Su an ev WiFi'sindeki herkes (misafir dahil) erisebiliyor. n8n 5678'i zaten dogru yapiyor, 8000'i ona esitle. Uzaktan erisim SSH tunnel ya da Tailscale ile. 3031 ve 8790'i da kontrol et, LAN'da gercekten gerekmiyorsa localhost'a bagla.
- [ ] Ekran kilidini System Settings'ten dogrula, kapaliysa ac: uyku/ekran koruyucu sonrasi sifre hemen ya da 1 dakika icinde istensin. Auto-login ile uyumlu, cunku auto-login sadece boot'ta gecerli, bu da "biri kapagi acti" durumunu kapatir.
- [ ] KARAR BURAK'A AIT, onsuz yapma. FileVault kapali ve macOS FileVault ile auto-login'i birlikte calistirmiyor, ikisinden biri. FileVault acik: disk sifreli, fiziksel erisim artik veri erisimi degil, ama elektrik kesintisinde makine unlock ekraninda kalir ve biri sifreyi yazana kadar tum ajanlar duser. FileVault kapali: 7/24 otonom reboot boyle calisiyor, ama makinede ASA imza key'i, finance agent verisi ve bir yigin API key plaintext dotenv'lerde. watercleaner-7a onerisi: FileVault acik arti kucuk UPS, ikisini de kazandirir. Karar bekliyor.
- [ ] Air icin Tailscale ACL + tag, ve Tailscale SSH'i ac (bugun kapali, advertised SSH host key yok). Erisim kontrolu tek yerde merkezi olarak iptal edilebilir hale gelir, makinelere dagilmis authorized_keys'e bagli kalmaz.
- [ ] Deco mesh'te ayri misafir WiFi, ziyaretciler LAN'a acik servislere ulasamasin.
- [ ] YAPMA (acikca): Superonline statik IP ile Deco'dan Air'e SSH ya da baska port-forward. Air zaten Tailscale ile her yerden, hucresel agdan, baska ulkeden erisilebilir, statik IP ek erisim getirmez, port-forward makinenin SSH'ini internetteki her tarayicinin onune koyar. Statik IP sadece Tailscale'in relay yerine direkt yol secmesine yarar (hiz meselesi). Gercekten public inbound gerekirse (ucuncu partiden n8n webhook gibi) dogru arac Cloudflare Tunnel ya da Tailscale Funnel, tek HTTPS yolu acar, router portu acmaz.
- [ ] Ayri not: makinedeki secret'lar plaintext dotenv. Yukaridaki FileVault karari bunun kabul edilebilir olup olmadigini belirler. FileVault kapali kalirsa Air'in durusu "eve giren herkesin okuyabilecegi bir sunucu", secret'lar buna gore secilmeli.

## Arastirilacak
- [ ] Yazilimcilar icin "20B" vergi muafiyetini arastir (Turkiye, yazilimci/gelistirici gelir vergisi istisnasi, sartlar ve basvuru)
- [ ] fieldtheory CLI olgunlasinca n8n Twitter bookmarks workflow'una entegre et

## Tamamlanan (Son)
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
