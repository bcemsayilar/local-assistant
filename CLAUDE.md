# Local Assistant - Kisisel Asistan Projesi

## Proje Amaci
Telegram botu (`@burakcembot`, Air'de 7/24). 2026-10-23 sadelestirmesinden beri iki yol var: `ruya`, `gunluk` ya da `spor <no>` ile baslayan mesaj modelsiz, kodla Obsidian vault'a yazilir (`assistant/notes.py`); geri kalan her sey (metin, gorsel, video, dosya, sesli not) Air'deki Claude Code oturumuna gider (`claude_bridge.py`). Yerel model (Ollama), RAG, GraphThulhu ve SearxNG bottan kaldirildi.

## Rol: genel yonetim oturumu (kurucu karari 2026-10-23)
Bu klasorde acilan oturum Mac Pro'daki iki yonetim oturumundan biridir: icerik disindaki her seyden sorumlu (altyapi, backend ve planlar, guvenlik, oturumlar arasi catisma, General App Guidlines, Data House, finans). Icerik `self-branding`'in, Mac Air `air-orkestrator`'un. Roller ve kurallar: `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md`.

## Sistem semasi (ZORUNLU, kurucu karari 2026-10-23)
Portfoyun canli semasi https://claude.ai/artifact/7RwAweEfyNQutzLT785WHY, kaynagi `docs/sistem-semasi.html`. Semadaki ana parcalardan biri degisince (yonetim oturumlari ve rolleri, Air servisleri ve zamanlayicilar, telefon erisim kurali, bot akisi, bulut servisleri, senkron klasorleri) ayni isin parcasi olarak guncellenir: once `docs/sistem-semasi.html` duzenlenir, sonra Artifact tool ile `url` bu adres verilip yayinlanir (once `action: read`), commit edilir. Ust satirdaki tarih ve kirmizi "bu gece degisti" noktalari her guncellemede yeni degisikliklere gore yeniden konur. Cizim kurali: kutular alt alta dizilmez, baglantilar gercek cizgiyle cizilir, cizgi etiketi dugume binmez. Self-branding de icerik tarafinda degisiklik yaparsa local-assistant'a haber verir.

## Teknoloji Yigini
- **Telegram**: python-telegram-bot v21+ (job-queue, ruya mesajlari 5 dk sonra silinir)
- **Notlar**: `assistant/notes.py`, ObsidianVault'a dogrudan dosya yazar (`ruya/`, `gunluk/`, `spor/Program N*.md` tablosu)
- **Ajan**: Air'de basliz ajan (`agentrun`: Claude, Codex ya da Gemini, limitte siradakine gecer), ayrinti "Claude kopru modu"
- **File Sync**: Syncthing (ObsidianVault iki makinede)
- **Dil**: Python 3.11 (venv)
- Ollama Air'de hala kurulu (qwen3.5:9b, lfm2.5:8b, nomic-embed-text) ama bot kullanmiyor; tek kullanicisi n8n Twitter Bookmarks (o da olu model `qwen3:4b`'ye bagli)

## LinkedIn Haftalik Post
- Yazim kurallari tek kaynak: `n8n/linkedin-automation/docs/linkedin-yazim-kurallari.md` (burada tekrarlanmaz)
- Arsiv ve stil referansi: `~/Desktop/Self Branding/LinkedIn/linkedin-postlari.txt`
- Uretim 2026-08'den beri `~/Mac-Projects/newsletter-project` (LinkedIn teaser, metni OpenAI yazar), detay o projenin `CLAUDE.md`'si

## Genel Kurallar
- Turkce commit mesajlari, teknik terimler Ingilizce kalabilir
- Commit mesajlarinda " ve : kullanma
- Commit mesajlarinda "fixed/done/completed" yerine "test/attempt/try" kullan
- Claude co-author ekleme
- Main branch'e dokunma (kullanici acikca belirtmedikce)
- Ruya, gunluk ve spor notlari buluta cikmaz (kodla yazilir); diger mesajlar Claude'a gider

## Altyapi - Makineler

Mac Air sunucusunun genel bilgisi (erişim, servisler, güvenlik): `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md`

### Mac Pro (gelistirme makinesi)
- **Kullanici**: buraksayilar
- **Proje yolu**: /Users/buraksayilar/Mac-Projects/local-assistant
- **Tailscale IP**: 100.109.79.90
- **Rol**: Gelistirme, test, kod yazma. Claude Code burada calisir.

### Mac Air (bu projenin Air tarafi)
- **Proje yolu**: ~/Projects/local-assistant
- **Rol**: Bot 7/24 calisir
- **LaunchAgent**: com.local-assistant.bot (KeepAlive + RunAtLoad)

### Deploy (bu proje)
Genel kalip home-server.md'de. Bu projede degisen dosyalar tar ile `~/Projects/local-assistant/` altina gonderilir, acilir, sonra `launchctl stop com.local-assistant.bot` (KeepAlive yeniden baslatir).

## Notlar (kodla, modelsiz)
- `ruya ...` / `rüya: ...` -> `ruya/` klasorundeki tek dosyaya tarihli callout; mesaj ve cevap 5 dk sonra sohbetten silinir
- `gunluk ...` -> `gunluk/YYYY-MM-DD.md`, saatli callout
- `spor 1` + satir satir `hareket: setler` (ya da `;` ile) -> `spor/Program 1*.md` tablosuna bugunun satiri; verilmeyen hareket `PROGRAM_DEFAULTS`, kalan metin Notlar sutunu. Numarasiz `spor ...` not sayilmaz, Claude'a gider
- Vault: iki makinede `~/ObsidianVault`, Syncthing folder `obsidian-vault`, iki yonlu
- GraphThulhu (`com.graphthulhu.server`) yalniz eski bot kullaniyordu, 2026-10-23'te durdurulmasi istendi

## Claude kopru modu (2026-10-04, 2026-10-28'den beri saglayici bagimsiz)
Ad eski kaldi: kopru artik `agentrun` uzerinden Claude, Codex ya da Gemini calistirir (siralama `AGENT_PROVIDER` ya da `~/.config/parallax/agent.json`, limitli saglayici atlanir). `ask_claude` adi `ask_agent`in takma adidir. Asagidaki Claude'a ozgu satirlar (`claude -p`, `CLAUDE_CODE_OAUTH_TOKEN`, TCC) yalniz Claude saglayicisi icin gecerlidir. Rehber: `General App Guidlines/agent-portability.md`.
2026-10-23'ten beri not anahtarlari disindaki her mesaj Claude Code'a gider ve buluta cikar: metin ("claude" oneki artik gerekmez, yazilirsa atilir), gorsel, video, dosya, sesli not ve ses dosyasi.
- Kod: `assistant/integrations/claude_bridge.py`, yonlendirme `telegram.py` (`handle_message` icinde `strip_prefix`, `handle_media`, `handle_voice`), `/yeni` yeni Claude oturumu.
- Instagram linki (2026-10-10): duz metinde instagram.com `/reel/`, `/p/`, `/tv/` linki varsa "claude" oneki aranmaz, `claude_bridge.harvest_prompt` tek seferlik bir Claude turu baslatir (`ask_claude(fresh=True)`, konusma oturumuna yazilmaz). Is akisi ve kurallar `~/Mac-Projects/parallax-content/shared/harvest/telefon-ajani.md` "Telegram hasadi".
- Calisma: Air'de `agentrun.run` (Claude icin `claude -p ... --dangerously-skip-permissions --resume <id>`, Codex icin `codex exec`, Gemini icin `gemini -p`), cwd ev klasoru (`~/CLAUDE.md` haritasi). Oturum kimligi `data/claude_sessions.json` (anahtar basina saglayici basina bir kimlik). Zaman asimi 30 dk.
- Token ve anahtarlar: Air `~/.config/parallax/agent.env` (600; `bin/agent setup` mevcut `.env` dosyalarindan alir), Claude icin `CLAUDE_CODE_OAUTH_TOKEN` ayrica `~/Projects/local-assistant/.env` ve `~/.zshrc` icinde.
- Medya `~/telegram-inbox/YYYY-MM-DD/` altina iner. Sesli not Air'de whisper-cli (`~/.cache/whisper/ggml-large-v3-turbo-q5_0.bin`) ile yaziya dokulur, metin ajana gider.
- Sesli cevap (2026-10-09): sesli nota (`msg.voice`) cevap hem ses hem metin olarak doner. `claude_bridge.speak()` Air'de `say -v Yelda` ile aiff uretir, ffmpeg libopus ile ogg'a cevirir, `run_claude(voice=True)` `reply_voice` ile yollar. Ses dosyasi (`msg.audio`) gonderilirse cevap sadece metin.
- TCC tuzagi (2026-10-05): Air'deki `claude` binary'si (`~/.local/share/claude/versions/<surum>`) Masaustu'ne ilk eristiginde macOS izin penceresi acar ve dosya erisimi pencere onaylanana kadar KILITLENIR; komut 120 sn sonra arka plana atilir, `claude -p` cikmaz ve 30 dk zaman asimi "bitiremedi" der. 2026-10-05'te pencere System Events ile onaylandi (`tell process "UserNotificationCenter" to click button "Allow" of window 1`). Claude yeni surume guncellenince binary yolu degisir, pencere tekrar cikabilir; "bitiremedi" gelirse once Air ekranina bak.
- Guvenlik: izin sormadan calisir, tek koruma `ALLOWED_USER_IDS`. Botun token'i Air'in anahtari sayilir.
- httpx INFO loglari bot token'ini URL icinde yaziyordu; `main.py`'de httpx WARNING'e cekildi, eski `bot-stderr.log` (238 MB) 2026-10-04'te bosaltildi. Token yine de dondurulmeli (BotFather /revoke).

## Supabase keep-alive (AWS, 2026-10-23)
Supabase Free plandaki projeler 7 gun hareketsiz kalinca durduruluyor. AWS Lambda `supabase-keepalive` (eu-central-1, hesap 573199225040, Activate kredisi) EventBridge `supabase-keepalive-12h` ile 12 saatte bir her projede herkese acik anahtarla tek satirlik REST okumasi yapar.
- Kod `aws/supabase-keepalive/handler.py`, kurulum `deploy.sh` (tekrar calistirmak guvenli, yonetici kimligi `vidberry/.env`). Proje listesi `projects.json` (git disi, sadece publishable ya da anon anahtar; secret ve hesap token'i yok).
- Kapsam: watercleaner (Clear Wave) ve wp-agent-studio (Parallax Technologies org, Free), pillowtale (bcsayilar org, Free). videoapp ve cvai_project Pro org'da, gerekmez.
- Sonuc CloudWatch `/aws/lambda/supabase-keepalive` (30 gun). 402 kota kisiti demek, istek veritabanina ulasmaz ve aktivite sayilmaz; Parallax Technologies org'u 2026-10-23'te `exceed_cached_egress_quota` ile kisitliydi.
- Yeni Free proje acilinca `projects.json`'a ekle, `deploy.sh` calistir.

## Proje Yapisi
```
local-assistant/
├── assistant/
│   ├── main.py              # bot baslatma
│   ├── config.py            # token, izinli kullanici, vault yolu
│   ├── notes.py             # ruya / gunluk / spor yonlendirici, kodla yazar
│   └── integrations/
│       ├── telegram.py      # handler'lar
│       └── claude_bridge.py # Air'deki Claude Code oturumu, whisper, sesli cevap
├── air-orkestrator/         # Air orkestratoru istek kutusu kodu
├── aws/                     # supabase-keepalive Lambda
├── n8n/                     # LinkedIn ve Twitter bookmarks workflow dokumani
├── docs/                    # development-log.md
└── projects/lifeOS/         # lifeOS arastirma notlari
```

## API Key'ler
- Tum key'ler `finance_agent.env` dosyasinda (local-assistant root)
- `MINIMAX_API_KEY_cemsayilar` - MiniMax API
- `OPENROUTER_API_KEY_cemsayilar` - OpenRouter API (coklu model erisimi)
- Gemini, Groq, Grok, Binance, Finnhub key'leri de ayni dosyada
- Key'leri kullanirken `finance_agent.env`'den oku, `.env`'ye ekleme

## n8n Otomasyon (Mac Air)
Mac Air sunucusunun genel bilgisi (erişim, servisler, güvenlik): `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md` (n8n'e localhost erisimi, SSH tuneli, REST API PUT ve API key orada).
- n8n: v2.8.3 (2026-10-02 dogrulandi), port 5678. Instance bu projenin ama icinde VidBerry, CV-Crafter ve UGC workflow'lari da var; onlarin dokumani kendi depolarinda
- LaunchAgent: ~/Library/LaunchAgents/com.n8n.server.plist
- Startup script: ~/start-n8n.sh
- Loglar: ~/.n8n/n8n.log ve ~/.n8n/n8n-error.log
- Workflow detaylari: `n8n/linkedin-automation/README.md`, `n8n/twitter-bookmarks/README.md`

### LinkedIn AI Post Workflow (S0RDiop6EVTj33AX)
- Haftalik AI newsletter verisini ceker ve ozetler. 2026-10-02 itibariyla `LLM - Write LinkedIn Post`, `Format Email HTML`, `Gmail - Send Post` node'lari DISABLED; post yazimi ve mail yok (Faz 2 uygulanmis)
- Kaynak: AlphaSignal + AI News (Gmail)
- LLM (Summarize node'u): OpenAI gpt-4o -> Gemini gemini-3.1-pro-preview -> Groq llama-3.3-70b -> Mistral, ilk basarili kullanilir
- Schedule: Pazartesi 09:00 Istanbul
- Webhook tetikleme: `ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 elifberraksayilar@100.108.136.36 "curl -s http://localhost:5678/webhook/linkedin-trigger"`
- Gmail body sorunu: HTTP Request node ile Gmail API dogrudan cagirilir (n8n Gmail node body'yi kesiyor)
- Detaylar ve teknik notlar: `n8n/linkedin-automation/README.md`

### Twitter Bookmarks Digest (gDUBYcStVPkPni3C)
- Haftalik Twitter bookmark ozeti -> kategorize email
- Kaynak: Twillot JSON export (manuel, bookmarks.json). Air'deki dosya 2026-02-28'den beri guncellenmedi, yani haftalik calisma yeni bookmark bulmadan bitiyor
- LLM: Ollama `qwen3:4b` (127.0.0.1:11434). Bu model 2026-10-02'de Air'de YUKLU DEGIL; yeni bookmark gelirse kategorize adimi hata verir
- Schedule: Pazar 20:00 Istanbul
- Webhook tetikleme: `ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 elifberraksayilar@100.108.136.36 "curl -s http://localhost:5678/webhook/twitter-bookmarks-trigger"`
- State: n8n staticData (processedIds)
- Detaylar: `n8n/twitter-bookmarks/README.md`
