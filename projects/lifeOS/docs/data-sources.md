# lifeOS Data Sources — Kullanici Envanteri

> Burak'in 2026-05-31'de paylasti veri kaynaklarinin tam listesi.
> Her kayit: ne icerigi var + nasil erisilir + zorluk seviyesi.

## 1. Notion
- **Icerik:**
  - Yillar icinde kaydedilen Twitter + LinkedIn postlari
  - Tatil notlari, yillik hedef notlari
  - Kucuk arastirmalar, todo listeleri
  - Gunluk ruya notlari (eski donem; son 2 ay Obsidian'da)
  - Film/dizi/kitap listeleri
- **Erisim:** Notion API (OAuth), n8n native node mevcut
- **Zorluk:** Dusuk — built-in connector mevcut
- **Onem:** Yuksek (ikinci beyin)

## 2. Mac Pro Lokal Dosyalar
- **PEAKUP icerikleri:**
  - Tum proje dosyalari (kod, belge, sunum, egitim)
  - Musteri bazinda klasorlenmis danismanlik projeleri (teklifler, sozlesmeler, kodlar, sunumlar)
  - Hazirlanan sunumlar, egitimler
- **Side projeler:**
  - VidBerry: uygulama + sosyal medya calismalari + kod
  - CV-Crafter: website + arastirmalar + sosyal medya + kod
  - benburakcem Instagram: uretilen icerikler, notlar, egitimler, CapCut dosyalari
- **Ozgecmisler**
- **Erisim:** Filesystem (Python + watchdog), format-spesifik extractor (PDF, DOCX, MD, kod)
- **Zorluk:** Orta — selective indexing gerek, GB seviyesi
- **Onem:** Yuksek (is + side hustle aktif sermaye)

## 3. Obsidian Vault (~/ObsidianVault)
- **Icerik:**
  - CV-Crafter proje gunlugu (hangi gun ne yapildi)
  - Spor notlari (sport_log ile yazilan)
  - Agent'in yazdigi notlar (daily_log, dream_log)
  - Son 2 ayin ruya notlari
  - Ozel bilgiler
- **Erisim:** Mevcut local-assistant zaten okuyor + GraphThulhu MCP graph traversal
- **Zorluk:** En dusuk — zaten parse edilebilir, lokal, yapilandirilmis, Syncthing ile iki yonlu sync
- **Onem:** Yuksek

## 4. ChatGPT + Claude Desktop + Claude Code Konusma Gecmisi
- **Icerik:**
  - Izlenen filmler, saglik/spor sorulari
  - PEAKUP, CV-Crafter, VidBerry, benburakcem proje arastirmalari
  - Detayli teknik chat'ler
- **Erisim:**
  - **ChatGPT:** Resmi export — Settings > Data Controls > Export. JSON dump.
  - **Claude Desktop:** Resmi export YOK. Anthropic conversation history API'si var ama dokumante degil.
  - **Claude Code:** Lokal JSONL dosyalar — `~/.claude/projects/*/*.jsonl`, ulasilabilir.
- **Zorluk:** Yuksek — programmatic alma sinirli. **Buyuk olasilikla elle alip iceri pump etmek gerek.**
- **Onem:** Yuksek (detayli reasoning ve arastirma kayitlari)
- **Strateji:** Manual periodic import. Her hafta/iki haftada bir export + lifeOS'a yukle.

## 5. iPhone Film Rulosu (Photos)
- **Icerik:** Yillara yayilan foto/video, screenshot (cogu Twitter/LinkedIn save), yemek/manzara/insan
- **Erisim yollari:**
  - iCloud Photos export → lokal Photos.app library (~/Pictures/Photos Library.photoslibrary)
  - Image Capture / AirDrop / Swift Photo Library API
  - Multimodal LLM (LLaVA, Qwen2-VL, Llama 3.2 Vision) ile foto -> metin
- **Zorluk:** En yuksek — RAM ve compute agir, indexing maliyetli
- **Onem:** Orta — selective indexing (screenshot klasoru oncelikli)
- **Strateji:** Once screenshot'lar (semantic save value en yuksek), sonra belirli album/klasorler. Tum library hayir.

## 6. Twitter + Instagram Saves
- **Icerik:** Yillarca kaydedilmis post/bookmark
- **Kategori plani (kullanici belirledi):**
  - Teknik
  - Startup
  - Design
  - Beslenme
  - Hayat
  - Motivasyon
  - Icerik Uretimi
- Her ana kategorinin alt kirilimi olacak (henuz tanimsiz)
- **Erisim:**
  - **Twitter:** fieldtheory CLI (kurulu, 747 bookmark sync edildi)
  - **Instagram:** instaloader fragile (IG block atar). Instagram "Download your information" bulk export tercih (2-3 ayda bir manual).
- **Zorluk:** Orta (Twitter), Yuksek (Instagram - Instagram'in kendi politikasi yuzunden)
- **Onem:** Orta-yuksek
- **Strateji:** Ingestion sirasinda agent 7 kategoriye otomatik etiketler.

## 7. Finansal Dashboard
- **Icerik:** Aylik Is Bankasi banka + kredi karti hesap dokumu, Mac Air'da tablo + dashboard
- **Erisim:** Mevcut, kullanici elle besliyor (Claude ile birlikte aylik analiz)
- **Zorluk:** Dusuk
- **Onem:** Yuksek (kararsal degerli)
- **Strateji:** Mevcut tabloyu lifeOS'a referans kaynagi olarak baglamak. "Su ay X kategoride harcamam?" sorgu.

## 8. Akilli Saat + Telegram Manuel Giris
- **Akilli saat (Apple Watch):**
  - Antrenman suresi, kalori, uyku
  - Apple Watch -> HealthKit -> CSV/JSON export (Health Auto Export gibi araclar)
- **Manuel (Telegram):**
  - Foto + mesaj — agent zaten parse ediyor (daily_log, sport_log, dream_log)
  - Mevcut local-assistant pipeline'i devam edecek
- **Zorluk:** Orta (HealthKit export script gerek)
- **Onem:** Yuksek (kisisel saglik + alistirma takibi)
- **Strateji:** HealthKit + manuel telegram ayni "personal-state" namespace altinda topla.

---

## Ozet — Faz Plani Onerisi

1. **Faz 1 (kolay):** Obsidian + Mac Pro lokal dosyalar
2. **Faz 2:** Notion (API connector)
3. **Faz 3:** Chat history (manual import: ChatGPT export + Claude Code JSONL)
4. **Faz 4:** Twitter saves (fieldtheory hazir) + auto-categorization
5. **Faz 5:** Finansal + akilli saat + Telegram input birlestirme
6. **Faz 6:** Instagram saves (manual periodic bulk)
7. **Faz 7:** iPhone Photos (selective: screenshot + belirli album)

## Onemli Notlar

- **Programmatic erisim olmayan kaynaklar (manual import sart):**
  - Claude Desktop chat history
  - Instagram saves (rate limit + ToS)
  - iPhone Photos (selective, batch)
- **Programmatic ama dolaylı:**
  - ChatGPT (resmi export, tek seferlik bulk)
  - Claude Code (lokal JSONL parse)
- **Tam programmatic:**
  - Notion API
  - Google Drive API
  - fieldtheory (Twitter)
  - Obsidian (lokal file)
  - Apple Watch (HealthKit export script)
  - Finans dashboard (mevcut Mac Air tablosu)
