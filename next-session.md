# Next Session - Devir Notu (guncel: 2026-10-27 gece)

Once `~/.claude/CLAUDE.md` (global kurallar, yonetim yapisi, yetki devri, kurucuya bildirim), sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md` ve `home-server.md`. Servise dokunmadan once `service-access.md`. Sistem semasi https://claude.ai/artifact/7RwAweEfyNQutzLT785WHY (kaynak `docs/sistem-semasi.html`). Acik isler `TODO.md`'de; bu dosya yalniz devir notu.

## Acik ve bekleyen (oncelik sirasiyla)

- **Temizlik turu:** 2026-10-27 21:20'de SSH'tan `ig-temizlik/run.py --force` ile baslatildi (limit yuzunden 26 ve 27 Ekim turlari calismamisti, iki gunluk birikim). Bitince kurucuya rapor: her hesapta islenen ve kalan reel, `tetik-bekleyen.md` acik huniler, turun BITTI mi SURUYOR mu dedigi. Kurucu "tum hesaplarda islenmemis reel kalmadiysa yeni bilgilerle is yapacagim" dedi. Log `~/android-agent/web/ig-temizlik.log`, ledger `parallax-content/shared/harvest/ledger.md`.
- **app-fabrikasi TestFlight:** Distribution imzasi 2026-10-27 gece acildi (kurucu Always Allow dedi, GUI tmux'tan pencere cikmadan imzalandi). af ASC urunleri (IAP `com.buraksayilar.asshot.unlock`, abonelik `com.buraksayilar.onscript.yearly` grup "Onscript Pro") hazir olunca iki uygulamayi arsivleyip TestFlight'a yukleyecek; build numaralari ve urun kimlikleri gelince app-registry'ye islenir.
- **Kurucuyla insanli test:** af STATUS'unda liste (As Shot yuzle olcum, ayna, dosyalar, AirPrint, sandbox satin alma; Onscript gercek sesle takip ve iki kipte ses seviyesi, Ses+Kayit'ta ses -50 dB supheli). Sandbox hesabi `cemsayilar@peakup.org`, parola Air ajan zincirinde `apple-sandbox:cemsayilar@peakup.org`.
- **Ikonlar:** Onscript O3 + orta satirin soluna beyaz oynat oku (kurucu secti), koyu App Store icin iki kenar secenegi; As Shot yeniden tasarlaniyor, kurucunun begendigi "ID Photo-Passport Photo" ikonundan esinti (renkli zemin, tek kalin beyaz sembol, vurgu noktasi). Adaylar Air `~/Projects/app-fabrikasi/arastirma/ikon/`; gelince Mac Pro'ya cekip kurucuya Preview'da goster.
- **parallax-kit sonraki surum (local-assistant isi):** secim satiri LocalizedStringKey ve accentSoft dolgu, sistem anahtarlarinin vurgu rengini kullanmamasi, koyu zeminde okunur pozitif renk (kontrast 4,32). Once `design-language.md`. Son etiket 0.1.1.
- **VidBerry Fal izni:** kurucu Telegram'dan yanlislikla af'ye yazmis, mesaj af'ye ulasmamis; kurucunun sozu vidberry-7f'ye aynen aktarildi, sonucu takip et.
- **Tailscale ACL'e 5900:** VNC yalniz LAN'da calisiyor; disaridan icin ACL'e 5900 eklenir (kurucunun admin paneli Safari'de acik olmali).
- **air-orkestrator:** iPhone 13 iproxy 8101 istegi (af birakti, simdilik Wi-Fi aktaricisi).
- **Kurucuda bekleyen sorular:** 250 dolarlik Claude kredisi nerede (claude.ai extra usage mi, Console API mi; API ise limitte Air islerini anahtara gecirme onerisi); Mixpanel dev ve prod ayri mi kalsin (global kural ayri diyor, 4 proje acik); Clear Wave "Comment APP" CTA degisimi; Coinbase Wallet ve Chrome Remote Desktop kurucunun Air'deki varsayilan Chrome profilinde duruyor.
- **Eski bekleyen:** watercleaner Supabase geri acma (TODO), Meta Ads walkthrough okuma (TODO).

## Bugun kurulan ve gecerli olanlar

- **Bildirim kapisi:** Air'den kurucuya her mesaj `bildirim/kurucuya_yaz.py`; Telegram'a yalniz hata ve karar, yalniz to-go modunda ya da Mac Pro nabzi (`com.local-assistant.nabiz`) bayatken. Kurucu "to go moduna gec" derse Air'de `python3 ~/Projects/local-assistant/bildirim/kurucuya_yaz.py mod to-go`, donuste `mod evde`. Yeni hatalar UserPromptSubmit kancasiyla bu oturuma duser. Kural `session-organization.md` "Notifying the founder".
- **Claude limit bekcisi:** `bildirim/claude_limit.py`; 25 Ekim haftalik limitinde gercekte calisti, isler kaybolmadi.
- **Orkestrator bekcisi:** `kosu.py` takilan kosuyu 5 ya da 11 dakikada oldurup bir kez yeniden dener; 2026-10-27'de gercekte calisti. Kok neden TODO'da.
- **Air kalici tmux:** `com.parallax.tmux-oturumlar` (Aqua) air-rc, app-fabrikasi, marketing-agent'i GUI oturumunda acar. tmux'u SSH'tan baslatma (codesign errSecInternalComponent). af'ye mesaj SendMessage `app-fabrikasi`; ulasmazsa tmux `send-keys`.
- **Air ekrani:** SSH ile `screencapture -x` calisir, takilan her seyde ilk is ekran goruntusu; System Events ile pencere tiklanir; parola pencerelerine betikle yazilamaz, kurucuya VNC acilir: `open -a "/System/Applications/Utilities/Screen Sharing.app" "vnc://elifberraksayilar@192.168.1.104"`, Standard. Sharing'deki Screen Sharing anahtarina dokunulmaz. Kurucu Air'in basina gonderilmez. Ayrinti `home-server.md`.
- **Air ekranini temiz tut:** bos Terminal pencereleri kapatilir (kurucu iki kez uyardi); Terminal pencere geri yukleme kapali.
- **Kablo:** 17 Pro Air'in kendi portunda C-C; hub'in ikinci USB-C'si PD (yalniz sarj, veri yok). `home-server-telefonlar.md`. Air sarji hub PD'den, AlDente %80'de tutar.
- **Instagram web:** benburakcem Air Chrome'da (CDP 9223) ajan zinciri sifresi ve WhatsApp koduyla acildi, "bu cihaza guven" isaretli. Ajan Chrome profilinden Coinbase Wallet kaldirildi.
- **Clear Wave kuyrugu:** 54 reel, 23 Kasim'a kadar; sabah "Comment APP", aksam "Link in bio".
- **As Shot ve Onscript kimlikleri:** app-registry.md (ASC, Sentry, Mixpanel, RevenueCat projfba681e7, IAP anahtari Q58D6NQ7MG).

## Kisisel / uyari

Kullanici sparring partner ister, kisa cevap ister. Urun adindan varsayma. Main'e commit icin acik izin gerekir (istisna: parallax-content). Geri donusu olmayan isler once onay. Yetkili kimligin varken kurucuya "panelden bak" deme.
