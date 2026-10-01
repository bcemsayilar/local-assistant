# Next Session - Devir Notu (guncel: 2026-10-02)

Bu not 2026-09-07 ile 2026-10-02 arasindaki uzun oturumun devridir. Oturum local-assistant dizininde acildi ama islerin cogu baska depolara ait; her maddenin yolu tam yazili. Onceki oturum bilinen bir zaaf gosterdi: baglam penceresi daraldikca dikkat dustu ve bir dokuman yanlis depoya yazildi. Bu yuzden asagidaki **DOGRULAMA LISTESI** tek tek kontrol edilecek, "yapildi" yazan hicbir seye dogrulamadan guvenme.

## ONCE BUNU OKU

- Global kurallar ve portfoy haritasi: `~/.claude/CLAUDE.md` (yeni dosya acmadan once ara, sahibi sec, Instagram hesap yetkisi kurali).
- Mac Air sunucusu: `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md` (kanonik).
- Instagram telefon ajani: `~/Desktop/parallax-content/shared/harvest/telefon-ajani.md` (kanonik), islem kaydi ayni klasorde `ledger.md`.

## 1. DOGRULAMA LISTESI: Mac Air bilgisi her dizinde atil ya da yanlis olmasin

2026-10-02'de Mac Air'in genel bilgisi tek yere (home-server.md) toplandi, diger yerlerde isaret satiri birakildi. Bu is kismen bir alt ajana yaptirildi, dogrulanmadi. Her satiri ac, kontrol et, sonucu bu listeye isle (dogru / duzeltildi / sorun).

Kontrol olcutu her dosya icin ayni: (a) genel Air bilgisi (SSH komutu, IP, Tailscale, RAM butcesi, servis/port listesi, hardening, n8n erisim yontemi, deploy kalibi) home-server.md'de var mi ve bu dosyadan silinmis mi, (b) yerine isaret satiri var mi, (c) projeye ozel olan bilgi yerinde duruyor mu, (d) yanlis bilgi kalmis mi (ozellikle n8n'e `http://100.108.136.36:5678` ile dogrudan erisim yanlis, n8n localhost'a bagli; "sudo yok" yanlis, NOPASSWD sudo var; 8000 "localhost" degil, tum arayuzlerde dinliyor).

- [ ] `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md` kendisi: servis tablosu Air'deki gercek `launchctl list` ve `lsof -iTCP -sTCP:LISTEN` ile birebir mi; alt ajanin ekledigi hostname (`Elifs-MacBook-Air`), pmset, crash reporter, kapatilan servisler listesi dogru mu; pillowtale satirlari (8790, `com.parallax.pillowtale-tts`, `com.parallax.pillowtale-tunnel`) dogru mu
- [ ] `~/.claude/CLAUDE.md`: "yeni dosya acmadan once", "Portfoy haritasi", "Home server", "Instagram hesap yetkisi" bolumleri; haritadaki her yol gercekten var mi
- [ ] `~/Mac-Projects/local-assistant/.claude/CLAUDE.md` (gitignored, git gecmisi yok, dikkatli): Air genel bolumleri silinmis mi, bot deploy ve n8n workflow detaylari kalmis mi, servis tablosundaki Android satiri dogru yola isaret ediyor mu
- [ ] `~/.claude/projects/-Users-buraksayilar-Mac-Projects-local-assistant/memory/MEMORY.md`: Mac Air bolumu isaret satirina inmis mi
- [ ] `~/Mac-Projects/local-assistant/TODO.md`: "Mac Air Hardening" listesi duruyor mu, basinda isaret var mi
- [ ] `~/Mac-Projects/local-assistant/next-session.md` (bu dosya): eski "MAC AIR ERISIMI" bolumu kaldirildi, kontrol et
- [ ] `~/Mac-Projects/local-assistant/docs/finance-tracker-akisi.md`, `n8n/linkedin-automation/README.md`, `n8n/twitter-bookmarks/README.md`, `projects/lifeOS/` dosyalari: alt ajan bunlara BAKMADI, Air IP'si geciyor, kontrol et
- [ ] `~/Mac-Projects/finance-agent/.claude/CLAUDE.md` (commit 0ce359a, dal `dev`), ayrica `docs/research/VPS_MIGRATION.md`, `STRATEGY.md`, `BACKTESTING.md`: alt ajan sadece CLAUDE.md'ye bakti
- [ ] `~/Desktop/vidberry/CLAUDE.md`, `docs/ops/cli-access.md`, `docs/marketing/instagram-dm-automation.md`, `docs/marketing/marketing-content-strategy.md` (commit 8ed3281, dal `development`)
- [ ] `~/Desktop/parallax-content/shared/knowledge/erisim.md`, `shared/pipeline-runbook.md`
- [ ] `~/Desktop/watercleaner/asa/README.md` (commit ca9b045, dal `dev`)
- [ ] `~/Desktop/pillowtale/docs/narration-voice.md` (pillowtale oturumu yazdi, commit 2ae2db6 ve 0c53bcf, dal `revenuecat-integration`)
- [ ] `~/Mac-Projects/resume-enhancer/claude_main/ai-content-marketing/*.md` ve `n8n-workflows/`: Air IP'si geciyor, hic bakilmadi
- [ ] Diger memory dizinleri: `~/.claude/projects/*resume-enhancer*/memory/`, `*finance-agent*/memory/`, `*New-Project-2*/memory/project_tts_engine_decision.md`: Air bilgisi geciyor, hic bakilmadi
- [ ] Tarama tekrar: `grep -rIl -iE "100\.108\.136\.36|elifberraksayilar|mac ?air" ~/Desktop ~/Mac-Projects ~/.claude --exclude-dir={node_modules,.git,.venv,venv}` ve cikan her dosyayi bu listeye karsi isaretle. Tarihli kayitlar (development-log, docs/status, changelog) degistirilmez.

## 2. INSTAGRAM: Android telefon ilk canli test (YAPILMADI, sirada bu)

Telefon hazir ama uzerinde henuz tek bir Instagram islemi denenmedi. Kurulum ve komutlar `telefon-ajani.md`'de.

Test adimlari:
1. Air'de `adb devices` telefonu gostersin; gnirehtet calisiyor mu (`~/android-agent/gnirehtet.log`), calismiyorsa baslat. Telefonda Instagram internete ciksin.
2. Instagram'i ac, hesap degistiriciden **benburakcem**'e gec (yetki: sadece benburakcem, appclearwave, buraksayilar, vid.berry). Telefonda kayitli baska hesaplar (elifbsayilar, peaka_boo2.o) var, DOKUNMA.
3. `uiautomator dump` ile DM listesini oku. kolton.hustles sohbetini ac: "Send me the link" ve "STATIC ADS" butonlari `uiautomator` dokumunde text olarak gorunuyor mu. Bu testin asil amaci bu: butonlu ManyChat mesajlari telefonda okunabilir ve basilabilir mi.
4. peter.visuals sohbetinde "Get the 25 hooks" butonu: basip acilan linki al (Gumroad, ajaykaja.gumroad.com, $0+ urun, e-posta istiyor). E-posta karari kullanicida, bekliyor.
5. Bir reel ac, scrcpy ile sesi Mac'e alip whisper ile transkript dene (iPhone tarafinda calisan yontem `shared/harvest/iphone-mirroring/acap.swift`).
6. Sonuclari `telefon-ajani.md`'ye isle: neyin calistigi, komutlar, tuzaklar.

## 3. INSTAGRAM: bekleyen isler (ledger: `parallax-content/shared/harvest/ledger.md`)

- Unsend bekleyen, **buraksayilar hesabindan** yapilacak (buraksayilar gondermis): kolton.hustles, alexanderkdavis & tailopez, misseatinggood, jiannacapri, hannahelizzzy x esti_app, peter.visuals karuseli. Hepsinin notu kayitli.
- Unsend bekleyen, benburakcem gonderdi: coach.joel.burgess reel'i (notu kayitli, DM'deki link alindi).
- Takipten cikilacak (onceden takipli degildi): coach.joel.burgess, peter.visuals. kolton.hustles'tan cikildi.
- peter.visuals Gumroad e-posta karari: bcsayilar@gmail.com ile alalim mi, kullaniciya soruldu, cevap yok.
- alexanderkdavis notu "guven dusuk": sessiz okunmustu, sesle tekrar okunmali.
- Joel'in YouTube egitimi (https://www.youtube.com/watch?v=jpD-GQlOEhc) transkripti teklif edildi, kullanici linki istedi, transkript istemedi.
- Hic girilmeyen sohbetler: buraksayilar <-> vid.berry, benburakcem <-> vid.berry (kullanici bugun prompt atti, burada), buraksayilar <-> cemworking2, buraksayilar <-> benburakcem'in ust kismi (19 Eylul'den itibaren cok mesaj var, sadece en yeni kisim islendi).
- Kayit yeri kurali: icerik belirler, alici hesap degil. Tablo `telefon-ajani.md` sonunda.

## 4. ANDROID TELEFON TEMIZLIGI (kullanici emri bekleniyor)

- Medya yedegi TAMAM, sayilar telefonla birebir: Air'de `~/android-backup/2026-10-02-galaxy-a12/` (24 GB; DCIM 492, Pictures 1114, Movies 156, Download 7, Music 4, Android/media 1787 dosya).
- Yapildi: animasyonlar kapali, ekran USB'de uyumuyor.
- **Bekleyen karar:** ~110 ucuncu parti uygulamanin kaldirilmasi ve medyanin silinmesi kullanicinin emrini bekliyor. WhatsApp sohbetleri ve Samsung Notes notlari ADB ile yedeklenemiyor; kullanici "sil" ya da "once yedekle" demedi. Instagram (`com.instagram.android`) ve gnirehtet (`com.genymobile.gnirehtet`) KALACAK.
- gnirehtet LaunchAgent degil, Air reboot olursa elle baslatilmali. Kalici yapmak acik is.

## 5. GUVENLIK VE KARARLAR (kullanicida)

- **FileVault kapali.** Air'de plaintext dotenv'ler, ASA imza key'i, pillowtale TTS_API_KEY. Oneri: FileVault ac + kucuk UPS. Detay home-server.md.
- **Pillowtale server.py fail-open:** Air'de `~/Projects/pillowtale-tts/server.py` satir 61, `TTS_API_KEY` bos gelirse auth tamamen kapaniyor. Oneri: anahtar bossa sunucu baslamasin (fail-closed). Isin sahibi Pillowtale, madde pillowtale TODO'sunda (pillowtale oturumu commit 0c53bcf, dal `revenuecat-integration`). Ama degisiklik Air'de yapilacak ve server.py pillowtale deposunda degil, Air'de duruyor, yani **koordineli yurutulecek:** pillowtale oturumuyla (SendMessage, ListAgents'ta `pillowtale-*`) kimin dosyayi duzenleyecegini netlestir, degisiklikten once server.py'nin yedegini al, `launchctl stop com.parallax.pillowtale-tts` ile yeniden baslat, sonra yan etkisiz testi tekrarla (anahtarsiz `DELETE http://127.0.0.1:8790/voice/yok-test-123` 401 donmeli; govdesiz POST /tts 422 doner ve yaniltir), sonucu pillowtale'e bildir ki TODO'yu kapatsin. Ayrica server.py'nin hicbir depoda versiyonlanmamis olmasi ayri bir eksik, pillowtale'e sor.
- Port 8000 (finance-agent) ve 8790 (pillowtale-tts) tum arayuzlerde dinliyor, firewall stealth dis erisimi kesiyor (olculdu). localhost'a cekmek acik is.
- `local-assistant/TODO.md` "Mac Air Hardening" listesinin tamami acik.

## 6. DIGER ACIK ISLER

- Claude Code Air'e kuruldu (2.1.287), giris yapilmadi; kullanici simdilik gerek yok dedi.
- Finans: 600k TL nakit tabana kadar TL'de biriktirme karari kullanicida. Taban dolunca doviz ve hisse mekanizmasini KILITLE (cekirdek endeks, AI uydu, altin, USD nakit; oranlar `~/Desktop/Data House/finance/baseline-analiz.md`'de yazili degil, sohbette konusuldu, yazilmali).
- Finance tracker dashboard'da 'iade'/internal satirlarini farkli renk gosterme (`~/Projects/finance-tracker/web/app.py`, Air) hala yapilmadi.
- Twilio iade maili: bcsayilar@gmail.com'da Twilio ile ilgili hicbir mail yok. Kullanici hangi adresten attigini soylemedi.
- Newsletter: Dunya Halleri artik bcsayilar@gmail.com'a geliyor (dunyahalleri@substack.com), kaynak olarak kullanilabilir. `~/Desktop/newsletter-project/TODO.md`'deki "Dunya Halleri kaynagi bulunamiyor" maddesi atil, guncellenmeli. Substack ikinci kanal fikri orada.
- Kimi'yi ucuz coding modeli olarak baglama (eski not, yapilmadi).
- Mac Air WiFi-uyku kopmasi kalici cozumu (eski not).

## 7. BU OTURUMDA YAPILANLAR (kisa)

- Newsletter: Eylul I (Substack + PEAKUP, gpt-4o / gpt-5.4 kor testi, jargon kotasi ve iki ayri ses icin prompt kurallari, GPT-6 Astra ve Navier-Stokes eklendi, gorseller). Eylul II Substack (Dunya Halleri 268, 5 gorsel). `newsletter-project/TODO.md` acildi.
- Data House: `personal.md`, `personal-instagram.md`, `ideas.md` (8 app fikri), `marketing/reklam-platformlari.md`, `opensource/opensource.md` (Unreal Agent), `finance/baseline-analiz.md`.
- Finans: finance.db'de 3 re-import kopyasi silindi (yedek `finance.db.bak-dedup-*`), 2025-2026 baseline cikarildi, tasarruf reconciliation (gercek ~18k/ay 2025, ~8k/ay 2026).
- Instagram iPhone Mirroring ile: 11 icerik islendi, 4 unsend, 3 yorum tetikleyici akisi. Prompt kutuphanesine Zeely 63 prompt + 63 referans gorsel ve 18 madde kontrol listesi; knowledge'a 30 re-hook kalibi; vidberry marketing'e esti_app formati.
- Safari + Instagram web API denendi: butonlu ManyChat mesajlari web'e gelmiyor (olculdu).
- Mac Air: Android telefon kuruldu (ADB, gnirehtet ile USB internet, Instagram 449 APK), Claude Code, adb/scrcpy/gnirehtet/apkeep.
- Dokuman sistemi: global CLAUDE.md'ye yeni yuva kurali ve portfoy haritasi; home-server.md (Mac Air kanonik); harvest/telefon-ajani.md; Mac Air bilgisinin repolardan temizligi (alt ajan + pillowtale oturumu); pillowtale TTS auth olcumu.
- watercleaner oturumuna Air SSH yardimi ve hardening listesi.

## KISISEL/UYARI

Kullanici sparring partner ister, yaltaklanma yok. Kisa cevap ister. Urun adindan varsayma. Metinleri OpenAI yazar, ben elle blog/post yazmam. Main'e commit icin acik izin gerekir.
