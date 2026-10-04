# lifeOS

> Kisisel "beyin" katmani: dagilmis veri kaynaklarini tek bir hafizada konsolide eden, hatirlayan, baglanti kuran, proaktif uyari verebilen partner-jarvis. Local-assistant'in dogal evrimi.
>
> Iki cikis kanali: **Claude Code** (gelistirici arayuzu) + **Telegram** (gunluk kullanim arayuzu).
> Tek backend, iki interface.

Status: **Acik proje #2** (paralel: LinkedIn newsletter projesi).

## Hedef Mimari

```
┌─────────────────────────────────────────────────────────────┐
│  DATA SOURCES (8 kategori)                                  │
│  Notion · Mac Pro · Obsidian · Chat History ·               │
│  iPhone Photos · Social Saves · Finance · Wearable+Manual   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────▼──────────┐
                │  INGESTION PIPELINE  │  (n8n + custom workers)
                │  - Connectors        │
                │  - Schedulers        │
                │  - File watchers     │
                └───────────┬──────────┘
                            │
                ┌───────────▼──────────────────────┐
                │  COGNITIVE LAYER (beyin)         │
                │  - Vector store (LanceDB)        │
                │  - Knowledge graph (Cognee/?)    │
                │  - Temporal/contradiction layer  │
                │  - Entity resolution             │
                │  - User profile distillation     │
                │  - Proactive triggers            │
                └───────────┬──────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       ┌──────▼───────┐          ┌────────▼────────┐
       │ Claude Code  │          │ Telegram bot    │
       │ (MCP server) │          │ (mevcut bot)    │
       └──────────────┘          └─────────────────┘
```

## Veri Kaynaklari (Kullanici Envanteri - 2026-05-31)

### 1. Notion sayfalari
- Twitter + LinkedIn post archive (yillarca)
- Tatil notlari, yillik hedef notlari, kucuk arastirmalar, todo listeler
- Gunluk ruya notlari
- Film/dizi/kitap listeleri
- **Erisim:** Notion API (OAuth), n8n native node.
- **Sayisal:** Bilinmiyor — workspace listesi cikarmali.

### 2. Mac Pro lokal dosyalar
- **PEAKUP** — tum proje dosyalari: kod, belge, sunum, egitim. Musteri bazinda klasor.
- Danismanlik projeleri — teklifler, sozlesmeler, kodlar, sunumlar.
- Side projeler: VidBerry (app + sosyal medya + kod), CV-Crafter (site + arastirma + sosyal medya + kod), benburakcem IG iceriklerini + CapCut dosyalari + egitim notlari.
- Ozgecmisler.
- **Erisim:** Filesystem (Python script + watchdog), formata gore (PDF, DOCX, MD, kod) farkli extractor.
- **Sayisal:** Buyuk, GB seviyesi olabilir — selective indexing gerekli.

### 3. Obsidian vault (~/ObsidianVault)
- CV-Crafter proje gunlugu (gunluk neler yapildi)
- Spor notlari (sport_log ile yazilan)
- Agent'in yazdigi notlar (daily_log, dream_log, vb)
- Son 2 ayin ruya notlari
- Ozel bilgiler
- **Erisim:** Mevcut local-assistant zaten okuyor. fs entegrasyonu mevcut. GraphThulhu MCP graph traversal icin var.
- **En kolay kaynak** — zaten parse edilebilir, lokal, yapilandirilmis.

### 4. ChatGPT + Claude Desktop chat history
- Izlenen filmler, saglik/spor sorulari, PEAKUP, CV-Crafter, VidBerry, benburakcem proje arastirmalari.
- **ChatGPT:** Resmi export ozelligi var — Settings > Data Controls > Export. JSON dump alir.
- **Claude Desktop:** Resmi export yok. Anthropic conversation history API'sini deneyebiliriz, yoksa manual scrape.
- **Stratejik karar:** Bir kerelik retroaktif dump + sonraki sohbetlerin canli yakalanmasi. Canli yakalama icin Claude Desktop'a MCP server bagli olmali (lifeOS kendisi MCP server olur).

### 5. iPhone film rulosu
- En zor kaynak.
- **Cozum yollari:**
  - **iCloud Photos export → lokal Photos.app library** (~/Pictures/Photos Library.photoslibrary) → SQLite + medya dosyalari okunabilir.
  - **Photos AirDrop / Image Capture / Photo Library API (Swift)** — selective sync.
  - **Local multimodal LLM:** LLaVA, Qwen2-VL, Llama 3.2 Vision — fotograf icerigini metne cevirebilir (object/scene detection + OCR + caption).
  - **Ram butcesi sorunu:** Mac Air 8GB'da multimodal model RAM kullanir — Mac Pro'da pipeline calistirmak daha mantikli, sonra ozet metni Mac Air'a aktarmak.
- **Selective indexing:** Tum 10K+ fotograf degil, sadece screenshot'lar (cogu zaten tweet/post save) ve belirli klasor/album'ler.

### 6. Sosyal medya kaydedilenleri (Twitter + Instagram saves)
- **Kategoriler (kullanici belirledi):** Teknik, Startup, Design, Beslenme, Hayat, Motivasyon, Icerik Uretimi.
- Her birinin alt kirilimi olacak.
- **Erisim:**
  - Twitter: fieldtheory CLI (zaten kurulu, 747 bookmark sync edildi). JSON dump.
  - Instagram: instaloader fragile, Instagram Data Download (manual periodic) tercih.
- **Auto-classification:** Ingestion sirasinda Ollama'ya "su 7 kategoriden hangisi?" diye sor, tag'le.

### 7. Finansal dashboard
- Aylik Is Bankasi banka + kredi karti hesap dokumu, Mac Air'de tablo + dashboard.
- **Erisim:** Mevcut, kullanici elle besliyor (Claude ile birlikte analiz).
- **Yapilacak:** Mevcut tabloyu lifeOS'a referans kaynagi olarak baglamak. "Su ay X kategoride harcamam ne kadardi?" sorgu yapilabilir.

### 8. Akilli saat + manuel giris (Telegram)
- **Akilli saat:** Antrenman suresi, kalori, uyku. Apple Watch -> HealthKit -> export (Health Auto Export uygulamasi gibi araclarla CSV/JSON).
- **Manuel:** Telegram'a foto + mesaj — agent zaten parse ediyor (daily_log, sport_log, dream_log).
- **Birlestirme:** HealthKit verisi + manuel girdileri ayni "personal-state" namespace altinda topla.

## Cogntive Layer Eksiklikleri (Mevcut local-assistant'in Sahip Olmadigi)

1. **Temporal reasoning** — "Mart'ta X dedim, Mayis'ta tersini" cozumlemesi.
2. **Contradiction resolution** — celisen bilgileri yontemli isaretle.
3. **Entity-aware retrieval** — "Pekaup'taki X client" cross-source (Notion + Drive + Telegram + email).
4. **Proactive triggers** — agent kendiliginden "buna geri donmek istemistin", "su iki not celiskili", "spor program X gunden beri yapilmiyor".
5. **Auto-categorization** — gelen icerigi 7 kategori + alt kirilimlara klasifiye.
6. **Personal profile distillation** — stable facts (boyu, hedefleri, kronik dosyalar) vs son aktivite (bu hafta neler) ayri tut.

## STRATEJI PIVOT (2026-06-05)

Cognee denendi, **Mac Air'da sürdürülebilir değil**:
- 4B model schema validation gecmiyor (kucuk model sinirlamasi - opensource.md'de teyit edilmis)
- 9B model 10dk+ pipeline tamamlanamadi, RAM/model load davranisi tutarsiz
- Docker overhead + structured output zincirleri Mac Air 8GB icin agir

**Yeni rota: PewDiePie Odysseus** (31 May 2026 yayinda, 55K star, MIT).
- Native Apple Silicon install (Metal GPU)
- ChromaDB + fastembed ONNX memory (Ollama embedding'e bagimsiz, schema sorunu yok)
- Hazir: chat, agent (opencode), memory/skills, email IMAP/SMTP triage, calendar CalDAV, notes/tasks cron, deep research, documents, compare, cookbook (donanim taramasi + model onerisi), PWA mobile
- Eksik kaynaklar (yine yazilacak): Notion, Drive, Twitter saves, Instagram, iPhone Photos, Obsidian vault baglama, mevcut Telegram bot entegrasyonu

Repo: https://github.com/pewdiepie-archdaemon/odysseus

## Eski Aday Stack Karsilastirma (referans)

| Tool | Repo | + | - | Karar |
|---|---|---|---|---|
| **Cognee** | topoteretes/cognee | Knowledge graph + temporal + RAG one-stop. Docker compose. Supermemory'nin en yakin acik muadili | Postgres + vector DB istiyor; daha agir | Birinci aday |
| **Mem0** | mem0ai/mem0 | Saf, kucuk, Python MIT, mevcut local-assistant'a hizli entegrasyon | Connector yok, ingestion sen | Hibrit aday (mem semantik katmani) |
| **Letta** | letta-ai/letta | Agent-centric, persistent context | Agent framework, knowledge hub icin overkill | Bypass |
| **Zep Community** | getzep/zep | Temporal + facts + contradiction. Semantik en yakin | Community version siyrik | Ikinci aday |
| **Custom on local-assistant** | LanceDB + LlamaIndex + Ollama | Tam kontrol, zero vendor, mevcut stack | Tum semantic katmani sifirdan yazmali | Hibrit aday |

**Onerim:** **Cognee** + **mevcut local-assistant interface** + **n8n ingestion**. Cognee bizim Supermemory'nin yerini alir. Mac Air'a Docker compose ile cikarilabilir, RAM butcesi test edilmesi gerek.

## Faz Plani (Iterative, Tek Adimda Tum Sistem Degil)

NOT: Bu plan 2026-06-05 pivotundan ONCE, Cognee varsayimiyla yazildi. Pivot sonrasi aday Odysseus; Cognee adimlari atil.

### Faz 0: Karar + Prototip Olarak Tek Kaynak
- Cognee Mac Air'da Docker ile ayaga kalkar mi? RAM testi.
- Ornek 100 Obsidian notu yukle, retrieval/temporal test et.
- Mem0 da paralel test, sade interface karsilastir.
- Karar: Cognee mi, Mem0 + custom mu?

### Faz 1: Obsidian + Mac filesystem
- En kolay iki kaynak. File watcher + Cognee ingest pipeline.
- Mevcut local-assistant tool olarak Cognee'yi cagirir, "lifeOS_search", "lifeOS_remember".
- Telegram bot uzerinden test.

### Faz 2: Notion connector
- n8n Notion node + OAuth.
- Workspace dump + incremental sync.
- Kategoriler kullanicidan: hangi sayfalar oncelik?

### Faz 3: Chat history retroaktif import
- ChatGPT export download → JSON parse → Cognee.
- Claude Desktop: arastir, mumkun degilse "bu noktadan itibaren MCP ile" devam et.

### Faz 4: Sosyal saves + auto-categorization
- fieldtheory dump → Ollama classifier → Cognee.
- 7 kategori + alt kirilim sistemi.

### Faz 5: Finansal + manual + saat
- HealthKit export script.
- Mevcut finans tablosunu kaynak olarak baglamak.

### Faz 6: iPhone photos
- En zor + ertelenebilir. Lokal multimodal pipeline + selective indexing.
- Mac Pro'da uretim, ozet Mac Air'a aktarim.

### Faz 7: Proactive layer + cikis kanali iyilestirme
- Daily review agent: "su konuya geri donmek istemistin".
- Cross-source query optimization.
- Claude Code MCP server'i hazir, Telegram bot hazir, Cognee Claude Code icin direkt MCP olarak baglanir mi?

Tek seferde olmaz, parca parca.

## Cikis Kanallari

### Claude Code
- Cognee'nin MCP server'i var mi? (Arastirilacak) Varsa direkt `.claude/mcp.json`'a eklenir.
- Yoksa MCP wrapper yazariz: lifeOS-mcp adli kucuk server, Cognee API'sini MCP olarak yansitir.

### Telegram bot
- Mevcut local-assistant zaten calisir. Yeni tool eklenir: `lifeOS_search(query)`, `lifeOS_remember(content, source, tags)`, `lifeOS_proactive_check()`.
- System prompt'a "lifeOS'a danis" mantigi.

## Sparring Notlari (Kullanici Adina Itiraz Edilmesi Gereken Yerler)

1. **"Tum kaynaklar tek sisteme" coju projede basarisiz olur.** Oncelik sec — Notion + Obsidian zaten ikinci beyninin %80'i. iPhone fotograflari ve sosyal saves later. Eger Faz 0-2 calisirsa, gerisi optional.

2. **Privacy ucurumu:** Tum bu veriler agregalandiginda saldiri yuzeyi 10x. Mac Air'in disari acik portu olmamasi sart. Cognee localde, dis baglanti yok.

3. **Chat history privacy:** ChatGPT/Claude Desktop konusmalarinda saglik, finansal, kisisel detaylar var. lifeOS'a yuklemeden once "hangi konularda ozel filtre?" karari ver. Bazi konusmalar lifeOS'a girmemeli.

4. **iPhone fotograf indexing maliyetli ve marginal.** 10K+ foto -> multimodal LLM ile metin -> embed = saatler suren is. Cogu fotograf "Lou Andreas-Salome ile selfie", "yemek", "kedi" gibi sey. *Sadece screenshot klasoru* veya *spesifik album* ile basla — full library degil.

5. **Ingestion'i once "manual import" olarak yap, sonra automate et.** Otomasyon yazip sonra "yanlis bilgi cekti" demek yerine, once elle 10 notu yukle, retrieval'i dogrula, sonra connector kur.

## Sıradaki Adim (Karar Bekleyen)

NOT: Asagidaki Cognee maddeleri 2026-06-05 pivotuyla atil kaldi (Cognee Mac Air'de denendi, surdurulebilir bulunmadi). Acik soru artik Odysseus'un Mac Air'de calistirilmasi.


- [ ] Cognee Mac Air'da Docker compose test → RAM butcesine sigar mi?
- [ ] Cognee MCP server'i var mi (Claude Code direkt baglanma)?
- [ ] Hangi kaynaktan baslayalim — Faz 1 (Obsidian + Mac fs) onerim, kullanici onayi?
- [ ] Chat history "neyi import etmemeli" filter listesi.

## Konusma Kaynaklari (Bu Karara Yon Veren)

- supermemoryai/supermemory repo — referans alinan kapali kaynak rakip.
- supermemory.ai/rag → design language inspiration (ayri konu, design-inspiration.md'ye).
- Ege Bese LifeOS X postu — isim ilhami + estetik dil referansi.
- Kullanicinin local-assistant CLAUDE.md'si — privacy prensibi.
- Kullanicinin veri kaynagi envanteri (2026-05-31) — yukaridaki 8 kategori.
