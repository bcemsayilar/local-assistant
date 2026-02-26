# LinkedIn AI Post Automation (n8n)

Haftalik AI newsletter'larini ozetleyip LinkedIn postu hazirlayan n8n workflow'u.

## Workflow ID
`S0RDiop6EVTj33AX` - "Weekly LinkedIn AI Post"

## Akis

```
Trigger (Schedule/Webhook/Manual)
  -> API Keys (Set node - LLM key'leri + styleExamples)
  -> Gmail - AlphaSignal (son 7 gun, 1 mail)
  -> Gmail - AI News (son 7 gun, 1 mail)
  -> Fetch Full - AlphaSignal (HTTP Request + Gmail OAuth2, format=full)
  -> Fetch Full - AI News (HTTP Request + Gmail OAuth2, format=full)
  -> Merge Newsletters
  -> Parse HTML & Extract (base64 decode + HTML strip + gorsel cikarma)
  -> LLM - Summarize (fallback chain, gemini-2.5-flash)
  -> LLM - Write LinkedIn Post (fallback chain, gemini-2.5-pro)
  -> Format Email HTML
  -> Gmail - Send Post (me@cemsayilar.com)
```

## Trigger'lar
- **Schedule**: Her Pazartesi 09:00 Istanbul
- **Webhook**: `GET http://100.108.136.36:5678/webhook/linkedin-trigger`
- **Manual**: n8n UI'dan test

## LLM Fallback Chain
Her iki LLM node'unda ayni sira: OpenAI -> Gemini -> Groq -> Mistral.
Ilk basarili provider kullanilir. Key yoksa veya hata verirse sonrakine gecer.

## Onemli Teknik Detaylar

### Gmail Body Sorunu
n8n Gmail node v2.1 `getAll` operasyonu mail body'sini dondurmuyor.
`payload.parts` ve `payload.body.data` flatted serialization sirasinda siliniyor.
Sadece `snippet` (ilk 200 char) ve `mimeType` kalir.

**Cozum**: Gmail node'dan sonra HTTP Request node ile Gmail API'yi dogrudan cagir:
```
GET https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}?format=full
```
- `authentication: predefinedCredentialType`
- `nodeCredentialType: gmailOAuth2`
- Credential ID: `smrImlBnhBgdsQEM` (Gmail account)

Bu sekilde `payload.parts[].body.data` (base64url encoded) tam gelir.

### Body Decode
Gmail API body'yi base64url formatinda dondurur:
```javascript
Buffer.from(data.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf-8')
```
Recursive `extractBody(payload)` fonksiyonu `text/html` ve `text/plain` MIME part'lari arar.

### Gorsel Filtreleme
Newsletter HTML'inden gorsel cikarilirken tracking pixel'ler, avatar'lar ve
kucuk ikonlar filtrelenir:
- `/o?`, `/open?`, `open?token` - tracking URL'ler
- `profile_images`, `avatar`, `_400x400` - profil resimleri
- `w_XX` (XX < 100) - kucuk substack ikonlari
- `.gif`, `1x1`, `spacer` - pixel tracker'lar

### Style Examples
API Keys node'unda `styleExamples` alani kullanicinin gercek LinkedIn postlarini icerir.
LLM bu ornekleri referans alarak ayni tonda post yazar.

**DIKKAT**: `n8n import:workflow` komutu calisirken styleExamples'i placeholder ile ezebilir.
Workflow guncellemelerini n8n REST API (`PUT /api/v1/workflows/{id}`) ile yapmak daha guvenli.

### n8n CLI vs REST API
- `n8n import:workflow` DB'yi gunceller ama calisan instance'in in-memory state'ini GUNCELLEMEZ
- REST API `PUT` hem DB'yi hem calisan instance'i gunceller
- Workflow degisiklikleri icin REST API tercih et

## n8n REST API Kullanimi

```bash
# API key'i al
N8N_KEY=$(sqlite3 ~/.n8n/database.sqlite "SELECT apiKey FROM user_api_keys LIMIT 1")

# Workflow oku
curl -s "http://100.108.136.36:5678/api/v1/workflows/S0RDiop6EVTj33AX" \
  -H "X-N8N-API-KEY: $N8N_KEY"

# Workflow guncelle (name, nodes, connections, settings zorunlu)
curl -s -X PUT "http://100.108.136.36:5678/api/v1/workflows/S0RDiop6EVTj33AX" \
  -H "X-N8N-API-KEY: $N8N_KEY" \
  -H "Content-Type: application/json" \
  -d @workflow-update.json

# Aktive et
curl -s -X POST "http://100.108.136.36:5678/api/v1/workflows/S0RDiop6EVTj33AX/activate" \
  -H "X-N8N-API-KEY: $N8N_KEY"
```

PUT payload'da sadece su alanlar olmali: `name`, `nodes`, `connections`, `settings`.

## Execution Data Okuma

n8n execution data'si `execution_data` tablosunda flatted formatinda saklanir:

```bash
# Data'yi dosyaya cek
sqlite3 ~/.n8n/database.sqlite \
  "SELECT data FROM execution_data WHERE executionId = 100" > /tmp/exec.json

# Node.js ile parse et (flatted gerekli)
node -e "
const flatted = require('.../n8n/node_modules/flatted');
const fs = require('fs');
const data = flatted.parse(fs.readFileSync('/tmp/exec.json', 'utf-8'));
const run = data.resultData.runData;
console.log(Object.keys(run)); // node isimleri
"
```

## Dosya Yapisi
```
n8n/linkedin-automation/
├── README.md          # Bu dosya
└── fix-workflow.py    # Workflow guncelleme scripti (ornek)
```
