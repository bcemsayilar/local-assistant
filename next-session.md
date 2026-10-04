# Next Session - Devir Notu (guncel: 2026-10-04)

Once `~/.claude/CLAUDE.md` (global kurallar, iki makine senkronu, tasima kurali, portfoy haritasi), sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md` (Mac Air: servisler, izinler, iPhone, Syncthing) ve `app-registry.md` (hangi app hangi backend). Instagram islerinin kanonik dokumani `~/Desktop/parallax-content/shared/harvest/telefon-ajani.md`, islem kaydi ayni klasorde `ledger.md`. Bu dosya sadece acik isleri tutar; yapilanlarin ayrintisi o dokumanlarda. Onceki surum (2026-10-02 dogrulama listesi) tamamlandi ve kaldirildi.

## Durum (2026-10-04 sonu)

- Mac Air ve Mac Pro Syncthing ile senkron: Data House, parallax-content, Parallax Technologies LLC, ObsidianVault, `~/.claude/CLAUDE.md`. Git commit ve push sadece Mac Pro'dan.
- Telegram botu (`@burakcembot`) iki beyinli: duz metin lokal qwen, "claude" ile baslayan mesaj, gorsel, video, dosya ve sesli not Air'deki Claude Code'a gider. Ayrinti: `.claude/CLAUDE.md` "Claude kopru modu".
- Air'de iPhone 17 Pro (WDA, `ios-on.sh` / `ios-off.sh`), Android (adb), Safari ve Chrome Instagram araclari hazir.
- buraksayilar <-> benburakcem sohbeti 2026-10-03'te tamamen islendi (303 oge), mesajlarin neredeyse hepsi geri alindi. Kalan: benburakcem 4 (leoreal.ai, hesamious, byjoeym, dijitalakcin) ve 2026-10-04 eabhabranded (islendi, unsend onayi Telegram'da bekliyor), buraksayilar 2.
- finance-agent PARKED (servisler durduruldu, `~/Mac-Projects/finance-agent/PARKED.md`).

## Acik isler (oncelik sirasiyla)

1. **Anahtar sizintilari (kullanici karari):** Fal anahtari vidberry ve vidberry-ios git gecmisinde, rotate edilmeli. cv-crafter-marketing n8n dosyasinda Google anahtari. Air'deki 16 n8n workflow'unun 12'sinde anahtarlar dugumlere gomulu, n8n credentials'a tasinmali. Pillowtale uygulamaya gomulu anahtarlarla kendi oturumunda ilgileniyor. Ayrinti `app-registry.md` "Violations and gaps".
2. **Merkezi anahtar deposu kurulumu: KARAR VERILDI, Infisical (acik kaynak). Kurulum bir sonraki oturumun ana isi.** Kullanici istegi: projelerin secret'lari tek yerde, Mac Air ve Mac Pro ayni kaynaktan guncel. Plan:
   - Barindirma: once Infisical Cloud ucretsiz katmani (Air 8 GB RAM, kendi barindirma Postgres ve Redis ister; limitleri kurulumda dogrula). Ileride gerekirse Air'de self-host.
   - Yapi: app basina bir proje (vidberry, pillowtale, watercleaner/Clear Wave, potty, cv-crafter, local-assistant, parallax-content, parallax-site, cemsayilar-site), her birinde `dev` ve `prod` ortami. Kaynak listesi: `General App Guidlines/app-registry.md`; bugun anahtarlarin cogu `~/Desktop/vidberry/.env` (bes urunun anahtarlari karisik, `REVENUECAT_API_KEY` aslinda Potty'nin), app `.env`'leri, Air'de `~/Projects/*/.env`, `~/.env`, local-assistant `finance_agent.env`.
   - Kurulum sirasi: (1) kullanici infisical.com'da hesap acar, `brew install infisical/get-cli/infisical` iki makineye, `infisical login`; (2) her `.env` CLI ile ilgili projeye ice aktarilir (`infisical secrets set --env=dev KEY=...` ya da dashboard'dan .env yukleme), degerler ekrana basilmaz; (3) Air servisleri icin proje basina salt-okunur Machine Identity, LaunchAgent'lar `infisical run --projectId ... --env=prod -- <komut>` ile ya da baslangicta `infisical export > .env` ile; (4) Mac Pro gelistirmede `infisical run -- ...`; (5) GitHub Actions ve Cloudflare icin Infisical entegrasyonu; (6) `.env` dosyalari elle yazilmaz, uretilir.
   - Rotate sirasi: Fal (`FAL_API_KEY`, `FAL_WEBHOOK_SECRET`, vidberry git gecmisinde, private repo), cv-crafter-marketing Google anahtari, n8n workflow'larindaki gomulu anahtarlar n8n credentials'a. Yeni degerler dogrudan Infisical'a yazilir. Pillowtale kendi anahtarlarini 2026-10-04'te yeniledi.
   - Sonra `General App Guidlines/`'a `secrets.md` (nasil kullanilir) ve global CLAUDE.md'ye tek satir isaret.
3. **ACIL: Mac Pro Masaustu iCloud sorunu (2026-10-04 olcum).** Sistem Ayarlari: iCloud Drive "Masaustu ve Belgeler" ACIK, "Optimize" KAPALI. Masaustunde 76.562 dosya "dataless" (Business 75.967, Freelance Projects 230, potty 203, vidberry-admin 149, parallax-content 13; `find ~/Desktop -flags +dataless`). iCloud indirme yapamiyor: Finder'da iCloud Drive acilmiyor, `brctl download` "No valid file provider found", `killall bird cloudd fileproviderd` sonrasi da dosya inmedi. parallax-content `.git` okunamiyor (`git fsck` mmap zaman asimi); calisma agaci Air'de Syncthing kopyasi olarak tam. YAPMA: "Masaustu ve Belgeler"i kapatmak (macOS dosyalari iCloud'da birakip yerel Masaustu'nu bosaltabilir). Siradaki adimlar: (a) kullanici iCloud.com > Drive > Desktop > Business'ta dosyalarin durdugunu dogrulasin, (b) Mac Pro yeniden baslatilsin (fileproviderd icin), (c) olmazsa depolari GitHub'dan `~/Mac-Projects`'e yeniden klonla, commit edilmemis calisma dosyalarini Air'deki Syncthing kopyasindan geri al; (d) sonra parallax-site ve (koordineli) parallax-kit tasinir. parallax-kit'i pillowtale ve watercleaner `../parallax-kit` ile kullaniyor.
4. **Push bekliyor:** local-assistant `9a1bc1e` (main, public repo, `docs/finance-tracker-akisi.md` kisisel bilgi nedeniyle gitignore) ve finance-agent `a82775d` (dev) commit edildi, push edilmedi.
5. **Telegram sesli cevap** (macOS `say`).
6. **Islenmemis sohbetler:** benburakcem <-> vid.berry, buraksayilar <-> cemworking2. Kullanicinin aradigi "marketing strateji" reel'i buraksayilar <-> benburakcem'de cikmadi, bu sohbetlerde olabilir.
7. **Mac Air hardening** (`TODO.md` ilgili bolum): FileVault karari, Tailscale ACL, misafir WiFi, log rotation.
8. **Syncthing surum farki:** Air 1.29.5, Mac Pro 2.0.11.

## Kisisel / uyari

Kullanici sparring partner ister, kisa cevap ister. Urun adindan varsayma. Main'e commit icin acik izin gerekir. Geri donusu olmayan isler (unsend, silme, takipten cikma, rotate) once onay.
