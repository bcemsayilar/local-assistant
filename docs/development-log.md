# Local Assistant - Development Log

## 2026-03-29 - Ollama KV Cache Compression + Nemotron-mini Denemesi

### KV Cache Compression (q8_0)
- Mac Air'deki Ollama'ya `OLLAMA_KV_CACHE_TYPE=q8_0` ve `OLLAMA_FLASH_ATTENTION=1` eklendi
- KV cache 2x sikistirma, konusma hafizasi yarisina iniyor
- Model boyutu degismiyor (qwen3.5:4b hala ~2.8GB)
- Daha uzun konusmalarda RAM tasarrufu sagliyor
- `launchctl setenv` + `.zprofile`'a eklendi (reboot sonrasi kalici)

### NVIDIA Nemotron-mini Denemesi
- **Model**: nemotron-mini:latest (2.5GB, Mamba-2 + Transformer hybrid)
- **Motivasyon**: 0xSero'nun 8GB tier onerisi, NVIDIA tool calling icin ozel egitmis
- **Sonuc**: BASARISIZ

**Test 1 - Ingilizce tool calling**:
- Tool call yapti ama format bozuk (nested arguments - arguments icinde tekrar function/arguments)
- Ollama'nin beklentisiyle uyumsuz

**Test 2 - Turkce tool calling**:
- Tool call tetiklemedi, direkt text olarak cevap verdi
- "Bugun hava guzeldi, parkta yurudum" - araci cagirmadan ozet gecti

**Test 3 - Turkce soru (tool call beklenerek)**:
- Yine tool call yok, text cevap

**Karar**: Nemotron-mini Turkce tool calling'de kullanisiz. qwen3.5:4b'nin Turkce anlama ve (bazi sorunlarina ragmen) tool calling yetenegi daha iyi. Model silindi.

**Dersler**:
- "Tool calling icin ozel egitilmis" demek Turkce'de de calisacak demek degil
- Kucuk modellerde dil destegi ve tool calling birlikte nadiren iyi calisiyor
- qwen3.5 Turkce icin hala en iyi secim 4B segmentinde
- TurboQuant (3-bit KV cache) llama.cpp mainline'a girince tekrar degerlendirilecek

## 2026-04-03/04 - Mac Air Baglanti Sorunlari ve Cozumleri

### Sorun
Mac Air surekli offline dusuyor - SSH ve ping timeout, Tailscale "offline" gosteriyor. Haftalarca sorunsuz calismisti, son 4-5 gunde basladi.

### Teshis
1. **hibernatemode 25** - macOS batarya tasarrufu icin RAM'i diske yazip tamamen kapaniyor. sleep 0 ayarli olsa bile hibernate ayri mekanizma. 36 gunde 106 kez uyuyup uyanmis.
2. **Stealth mode** - Firewall stealth mode ICMP ping'i engelliyor. Mac Air ayakta olsa bile ping timeout veriyor, "offline" saniyoruz.
3. **displaysleep WiFi oldurme** - Ekran kapaninca (displaysleep 15) WiFi chipset power save moduna geciyor, tum baglanti kopuyor. caffeinate bile yetmiyor.

### Uygulanan Duzeltmeler
```
sudo pmset -a hibernatemode 0      # hibernate tamamen kapali
sudo pmset -a autopoweroff 0       # otomatik guc kesme kapali
sudo pmset -a standbydelayhigh 86400
sudo pmset -a standbydelaylow 86400
sudo pmset -a networkoversleep 1   # ekran kapansa bile WiFi acik
sudo pmset -a displaysleep 0       # ekran kapanmasin (son care)
```

### caffeinate LaunchAgent (kalici)
~/Library/LaunchAgents/com.caffeinate.keepawake.plist olusturuldu
- `/usr/bin/caffeinate -d -i -s` (display idle + system idle + system sleep engelle)
- RunAtLoad + KeepAlive = reboot sonrasi da otomatik

### Ruya Notu Auto-Delete Sorunu
- misfire_grace_time 600s (10dk) -> 86400s (24 saat) olarak guncellendi
- Mac Air uyudugunda scheduler zamaninda calisamiyor, 10dk grace time asiliyor, mesajlar silinmiyordu
- Artik 24 saat icinde uyandiginda silme islemi calisiyor

### Ruya Notu Algilama Bug Fix
- loop.py'deki keyword-based ruya algilama kaldirildi
- Sadece "ruya notu" veya "ruya:" prefix'i ile tetikleniyor
- "ruyalar hakkinda ne dusunuyorsun" gibi sorular artik ruya notu olarak kaydedilmiyor

### Dersler
- `sleep 0` hibernate'i ENGELLEMEZ - ayri ayar (hibernatemode)
- Stealth mode + hibernate birlesince sorun teshisi cok zor: ping calismaz, SSH calismaz, Tailscale offline der
- macOS guncellemeleri pmset ayarlarini resetleyebilir - kontrol edilmeli
- M1 Air'de ekran kapaninca WiFi olumu bilinen donanim davranisi
- Bundan sonra Mac Air kontrolu ping yerine SSH ile yapilmali (stealth mode ping engelliyor)

## 2026-04-03/05 - Genel Calisma Ozeti

### Telegram Bot
- Ruya notu algilama: keyword-based -> prefix-only degistirildi (loop.py + prompts.py)
- Auto-delete misfire_grace_time: 600s -> 86400s (telegram.py)
- Deploy edildi, bot restart edildi

### Ollama
- KV cache compression aktif: OLLAMA_KV_CACHE_TYPE=q8_0, OLLAMA_FLASH_ATTENTION=1
- Nemotron-mini denendi, Turkce tool calling basarisiz, silindi
- .zprofile'a env var'lar kalici eklendi

### Mac Air Altyapi
- hibernatemode 25 -> 0 (hibernate kapali)
- autopoweroff 0, standbydelay 86400
- caffeinate LaunchAgent olusturuldu (com.caffeinate.keepawake)
- displaysleep sorunu tespit edildi (WiFi ekran kapaninca oluyor)
- Lokal IP degisti: 192.168.1.121 -> 192.168.1.109

### Finance Tracker
- 21 yeni islem eklendi (20 Mart - 4 Nisan, banka + kredi karti)

### LinkedIn Post Workflow
- n8n workflow tetiklendi, bulten verileri cekildi
- Gemini ozeti yetersiz geldi, ham bulten verilerinden manuel post yazildi
- Stil kurallari CLAUDE.md'ye eklendi
- Post dosyasi: linkedin-postlari.txt (Data House degil, Desktop/Self Branding/LinkedIn/)

### Arac Kurulumlari
- RTK (Rust Token Killer): brew install rtk && rtk init -g - Claude Code token tasarrufu
- fieldtheory CLI: npm install -g fieldtheory - Twitter bookmark sync (747 bookmark cekildi)

### Data House Dosya Organizasyonu
- tips.md 3'e bolundu: tips.md + opensource.md + ideas.md
- 15 yeni screenshot kategorize edildi
- 31 Twitter bookmark analiz edilip 17 tanesi dosyalara dagildi
- Dosyalar Desktop/Data House/ altinda

## 2026-11-16 ve 17 gece (kurucu uyurken, to-go modu; brief onaylari local-assistant)

Kurucu istegi: gece iki gorev (portfoy verimlilik denetimi; kisisel ve profesyonel kariyer ve hayat plani), ayrica TikTok reddinin cozumu, VidBerry reelinin bitirilmesi, ChatPlace ekran kayitlari.

### Baslatilan ajanlar (salt okuma, brief kurallari `ORTAK-KURALLAR` metniyle, local-assistant onayladi)
- Denetim A parallax-content, B project-benburakcem-ai ve cevresi, C Mac Air, D mobil uygulama depolari, E AWS ve yonetim depolari (Sonnet); sayi toplama ajani (Opus): gelir, kullanici, Instagram, huni.
- Diger oturumlara onaylanan brief'ler: self-branding arastirma A ve B, metin ve ses C, uretim D (uc dalga, taslak, yayin yok); dort reel kurgu brief'i (FreeLLMAPI icin uc guvenlik sarti); vidberry (Fal uzerinden grok, ABC kiyasi, reel v4); app-fabrikasi (as-shot ve onscript push, durum notlari).

### Yapilanlar
- Denetim sicili `docs/audit/ACIK-BULGULAR.md`: 34 acik bulgu (S-38 ile S-72), elzem sira ve kurucu sorulari basinda.
- Hayat ve kariyer plani git disinda: `~/ObsidianVault/Plan/2026-11-17_burakcem-plani.md`, olculen sayilar `2026-11-16_sayilar.md`.
- TikTok: ret notu okundu; `parallax-site` publisher sayfalarinda ikon, baslik ve kosul ile gizlilik linkleri basvuruyla eslestirildi (a74408e, canlida dogrulandi); kalan kurucunun elle cekecegi demo videosu ve portalda Web URL alani.
- Air yedegi as-shot ve onscript git paketlerini aliyor (aa812ed); ig-otomasyon canli kurallari dosyaya dokuldu, PITR acildi, huni durumu belgede duzeltildi (ig-otomasyon 07de9c5).
- Claude ikili dosyasi icin sabit yol betigi `bin/claude-sabit` ve Mac Pro LaunchAgent'i; Air tarafi air-orkestrator istegi 20261116-215146.
- `bin/mail gonder` ek destegi (`--ek`); ChatPlace'e imzali W-8BEN ile cevap gonderildi (kurucu onayiyla).
- App Store toplu 4.3 reddi: Onscript icin Apple'in dokuz sorusuna cevap gonderildi (ASC ic API, Safari oturumu).
