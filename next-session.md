# Next Session - Devir Notu (guncel: 2026-10-08)

Once `~/.claude/CLAUDE.md` (global kurallar, iki makine senkronu, tasima kurali, portfoy haritasi), sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md` (Mac Air: servisler, izinler, iPhone, Syncthing) ve `app-registry.md` (hangi app hangi backend). Instagram islerinin kanonik dokumani `~/Mac-Projects/parallax-content/shared/harvest/telefon-ajani.md`, islem kaydi ayni klasorde `ledger.md`. Bu dosya sadece acik isleri tutar; yapilanlarin ayrintisi o dokumanlarda. Onceki surum (2026-10-02 dogrulama listesi) tamamlandi ve kaldirildi.

## Durum (2026-10-04 sonu)

- Mac Air ve Mac Pro Syncthing ile senkron: Data House, parallax-content (iki makinede `~/Mac-Projects/parallax-content`), Parallax Technologies LLC, ObsidianVault, `~/.claude/CLAUDE.md`. Git commit ve push sadece Mac Pro'dan. App depolari artik `~/Mac-Projects/` altinda, Masaustunde degil.
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

7. **iCloud tasimasi sonrasi kalan kontroller:** git depolari ve `parallax-content` 2026-10-08'de `~/Mac-Projects/` altina tasindi, OneDrive kalintisi temizlendi, commitler push edildi; yontem ve dersler `General App Guidlines/ios-toolchain.md` "How this ended" bolumunde. Kalan: Mac Pro bir sonraki yeniden baslatmadan sonra `brew services list | grep syncthing` "started" mi (iki kez kapali bulundu) ve `fileproviderctl dump | grep -E "display name|reconciliation"` ile iCloud kuyrugu (2026-10-08 13:00 olcumu 75.517, baslangic 777.823). iCloud kuyrugunda kalan yaklasik 75 bin kaydin (2026-10-09 olcumu 74.673) yarisi 2026-09-29'dan beri `parentCreation` beklemesinde takili (sunucuda olup diskte ust klasoru olmayan kayitlar), diger yarisi hala iCloud altinda duran klasorlerden: `~/Documents/ComfyUI` (37.754 dosya, `.venv` dahil), `Freelance Projects/Project Directory/WhatsappAgent` (26.804 dosya), `Self Branding/project-benburakcem-ai/.git`, `~/Documents` altindaki kucuk git depolari (Landmarks, vidcrafter, AirGuard, GitHub/Peakup_Projects). Tasinip tasinmayacagi kullanici karari. Cop'teki root sahipli `OneDrive.app` kullanici karariyla duruyor.

## Kisisel / uyari

Kullanici sparring partner ister, kisa cevap ister. Urun adindan varsayma. Main'e commit icin acik izin gerekir. Geri donusu olmayan isler (unsend, silme, takipten cikma, rotate) once onay. Infisical ve benzeri agir secret yoneticisi istemiyor (2026-10-04); daha basit bir cozum isterse ayrica konusulur.
