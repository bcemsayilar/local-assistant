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
2. **Telegram sesli cevap** (macOS `say`). Gonderim test edildi 2026-10-04: Air'de `say -v Yelda -o x.aiff`, `~/bin/ffmpeg -c:a libopus`, Bot API `sendVoice` calisiyor. Kalan: botun cevabini sese cevirip gondermesi (hangi durumda sesli cevap verecegi karari)
3. **Islenmemis sohbetler:** benburakcem <-> vid.berry, buraksayilar <-> cemworking2. Kullanicinin aradigi "marketing strateji" reel'i buraksayilar <-> benburakcem'de cikmadi, bu sohbetlerde olabilir.
4. **Mac Air hardening** (`TODO.md` ilgili bolum): Tailscale ACL, misafir WiFi, log rotation. FileVault acilmayacak (kullanici karari 2026-10-04).

5. **Air ve Android icin sarj ve kablo duzeni plani (kullanici istegi 2026-10-05):** slink hub artik Android'de (ethernet modemde, PD sarjda), Air'in bir portu iPhone'da, digeri bos; Air sarj almiyor. Android telefon da hub'in PD'sinden sarj olmuyor gorunuyor (`dumpsys battery` USB powered false). Ihtiyac: Air icin sarj, telefon icin sarj artı ethernet, iPhone icin veri. Ayrinti home-server.md "Kablo duzeni".
6. **buraksayilar <-> vid.berry sohbeti (~30 oge, cogu VidBerry rakip reklami):** 2026-10-05 gecesi Android'den benburakcem'e iletilip web API ile toplu islenmeye baslandi; ledger'a bak.

7. **iCloud silme testi sonucu:** `~/Desktop/cemsayilar-site` 2026-10-06 00:29'da silindi, 2026-10-07'de Mac yeniden basladiktan sonra da geri gelmedi. Gercek kopya `~/Mac-Projects/cemsayilar-site`. Bir kez daha `ls ~/Desktop/cemsayilar-site` ile bak, yoksa kullanici onayiyla bu maddeyi sil.

8. **Masaustundeki git depolarini iCloud disina tasimak (kullanici karari 2026-10-07, tek cozum):** sorun aylardir suruyor. 2026-10-07 olcumu: Mac Pro yeniden basladiktan sonra iCloud indirme ve silme calisiyor, `bird` %0, swap 0, ama `fileproviderd` %100 CPU'da ve `fileproviderctl dump | grep reconciliation` iki kuyruk gosteriyor: 777.810 ve 1.152.411 kayit. Oturum basinda bu iki sayiya tekrar bak (dusuyor mu, sabit mi). **Tasimadan once yan etkileri arastir ve kullaniciya sun:** (a) Xcode proje yollari, `project.yml`, `Package.swift` yerel paket yollari (pillowtale ve watercleaner `../parallax-kit` kullaniyor), DerivedData; (b) Syncthing klasor yollari (parallax-content, Parallax Technologies LLC, Data House iki makinede `~/Desktop` altinda, Air tarafi da degismeli); (c) global ve proje `CLAUDE.md` atiflari, Claude proje hafizasi klasor adlari (`~/.claude/projects/-Users-buraksayilar-Desktop-<ad>`); (d) LaunchAgent, script ve `.env` mutlak yollari (vidberry `.env`'i Clear Wave ve parallax-content de okuyor); (e) acik oturumlar (`lsof -d cwd`); (f) eski kopyanin iCloud'dan geri gelme riski (`cemsayilar-site` ve PEAKUP silmeleri 2026-10-06'da geri gelmedi, kabukta `rm -rf` calisti, Finder "needs to be downloaded" diye reddetti). Yontem ve depo durum tablosu `~/Desktop/ICLOUD-GIT-HASARI-VE-TASIMA.md`. Sira onerisi: once kucukler (parallax-site, potty), en son vidberry.

## Kisisel / uyari

Kullanici sparring partner ister, kisa cevap ister. Urun adindan varsayma. Main'e commit icin acik izin gerekir. Geri donusu olmayan isler (unsend, silme, takipten cikma, rotate) once onay. Infisical ve benzeri agir secret yoneticisi istemiyor (2026-10-04); daha basit bir cozum isterse ayrica konusulur.
