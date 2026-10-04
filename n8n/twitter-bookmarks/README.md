# Twitter Bookmarks Weekly Digest (n8n)

Twitter/X bookmark'larindan haftalik kategorize ozet email'i olusturan n8n workflow'u.

**Durum (2026-10-02 olcum):** workflow aktif ve her Pazar "basarili" kosuyor, ama fiilen bos donuyor: Air'deki `bookmarks.json` 2026-02-28'den beri guncellenmedi, ve workflow'un kullandigi `qwen3:4b` Air'de artik yuklu degil (yuklu: qwen3.5:9b, lfm2.5:8b). Yeni bookmark gelirse Ollama adimi hata verir. Acik is `TODO.md`'de.

## Workflow ID
`gDUBYcStVPkPni3C` (workflow_id.txt dosyasinda da saklanir)

## Akis

```
Trigger (Schedule Pazar 20:00 / Webhook / Manual)
  -> Read Bookmarks (Execute Command - cat bookmarks.json)
  -> Parse & Deduplicate (Code - yeni bookmark'lari filtrele)
  -> Ollama Kategorize (HTTP Request - qwen3:4b, 127.0.0.1:11434)
  -> Format Email (Code - HTML email olustur)
  -> Gmail Send Digest (me@cemsayilar.com)
  -> Update State (Code - islenmis ID'leri kaydet)
```

## Trigger'lar
- **Schedule** - Her Pazar 20:00 Istanbul
- **Webhook** - `GET http://localhost:5678/webhook/twitter-bookmarks-trigger`, Air'in icinden. Mac Pro'dan: `ssh elifberraksayilar@100.108.136.36 "curl -s http://localhost:5678/webhook/twitter-bookmarks-trigger"`
- **Manual** - n8n UI'dan test

n8n localhost'a bagli; SSH tuneli ve tam SSH komutu: `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md`.

## Bookmark Toplama - Twillot

1. Chrome Web Store'dan Twillot extension'i yukle
2. Twitter/X'e giris yap
3. Bookmark'lara git, Twillot ile JSON export yap
4. Export dosyasini `bookmarks.json` olarak kaydet
5. Mac Air'e kopyala veya Syncthing ile sync et

### Dosya konumu (Mac Air)
```
~/Projects/local-assistant/data/twitter-bookmarks/bookmarks.json
```

### Beklenen JSON formati
```json
[
  {
    "text": "tweet content",
    "url": "https://x.com/user/status/123",
    "author": "username",
    "created_at": "2026-02-28T10:30:00.000Z"
  }
]
```

Parser esnek yazildi - `text/content/full_text`, `url/link`, `author/user/username/screen_name` field'larini otomatik algilar. Array veya `{bookmarks: [...]}` / `{data: [...]}` formatlarini destekler.

## Deduplicate Mantigi

n8n `$getWorkflowStaticData('global')` kullanilir:
- Her bookmark'un URL/ID'si `processedIds` array'inde saklanir
- Workflow DB'de persist eder, restart'ta kaybolmaz
- Ayni bookmarks.json ile tekrar calistirinca "yeni bookmark yok" donup durur
- Workflow silinip yeniden olusturulursa state sifirlanir

## Ollama Entegrasyonu

- Endpoint: `POST http://localhost:11434/api/generate`
- Model: qwen3:4b (2026-10-02'de Air'de yuklu degil, bkz Durum)
- stream: false (tek JSON response)
- Timeout: 180 saniye
- Prompt sonunda `/no_think` - qwen3 thinking modunu kapatir
- Kategoriler: AI/ML, Tech, Business, Turkiye, Diger

## Node Detaylari

| Node | Tip | Aciklama |
|------|-----|----------|
| Schedule Trigger | scheduleTrigger | Pazar 20:00 Istanbul |
| Webhook Trigger | webhook | GET /twitter-bookmarks-trigger |
| Parse & Deduplicate | code | require('fs') ile oku, staticData ile filtre, prompt olustur |
| Ollama Kategorize | httpRequest | POST 127.0.0.1:11434/api/generate (timeout 300s) |
| Format Email | code | Markdown->HTML, email template |
| Gmail Send Digest | gmail | me@cemsayilar.com'a gonder |
| Update State | code | processedIds'i staticData'ya kaydet |

## Yonetim Scripti

Script Mac Pro'da calisir ve n8n'e `http://localhost:5678` ile gider; once SSH tuneli ac (`ssh -L 5678:localhost:5678 ...`, komut home-server.md'de).

```bash
cd n8n/twitter-bookmarks/

# Workflow olustur (ilk kez)
python fix-workflow.py create

# Workflow'u aktif et
python fix-workflow.py activate

# Ornek veri ile test
python fix-workflow.py test      # sample-bookmarks.json -> Mac Air
python fix-workflow.py trigger   # webhook ile tetikle

# Guncelleme
python fix-workflow.py update    # Script'teki tanimi n8n'e push et
python fix-workflow.py status    # Durumu gor
```

## Test Proseduru

1. `python fix-workflow.py create` - Workflow'u olustur
2. `python fix-workflow.py activate` - Aktif et
3. `python fix-workflow.py test` - sample-bookmarks.json'u Mac Air'e kopyala
4. `python fix-workflow.py trigger` - Webhook ile tetikle
5. me@cemsayilar.com'a email geldi mi kontrol et
6. `python fix-workflow.py trigger` - Tekrar tetikle (yeni bookmark yok mesaji beklenir)

## n8n Ortam Degiskenleri
- `NODE_FUNCTION_ALLOW_BUILTIN=*` - start-n8n.sh'de (Code node'da require('fs') icin gerekli)

## Bilinen Kisitlamalar

- Twillot export formati degisirse Code node'daki parser guncellenmeli
- qwen3:4b uzun tweet listelerinde (50+) context limitine takili kalabilir
- staticData workflow silinince sifirlanir
- Ollama'ya ust uste cok istek giderse kuyruk olusur ve timeout verir (tek tetikleme yap)
- HTTP Request node 127.0.0.1 kullanmali (localhost IPv6'ya duser, Ollama IPv4)

## Dosya Yapisi
```
n8n/twitter-bookmarks/
├── README.md               # Bu dosya
├── fix-workflow.py          # Workflow CRUD + test scripti
├── sample-bookmarks.json    # Ornek test verisi (5 tweet)
└── workflow_id.txt          # n8n workflow ID (create sonrasi olusur)
```
