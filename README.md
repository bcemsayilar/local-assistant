# Local Assistant

Kurucunun Telegram botu (`@burakcembot`). Mac Air'de 7/24 calisir (LaunchAgent `com.local-assistant.bot`).

## Ne yapar

- `ruya ...`, `gunluk ...`, `spor <no> ...` ile baslayan mesaj modelsiz, kodla Obsidian vault'a yazilir (`assistant/notes.py`). Ruya mesajlari 5 dakika sonra sohbetten silinir.
- Geri kalan her sey (metin, gorsel, video, dosya, sesli not) Air'deki Claude Code oturumuna gider (`assistant/integrations/claude_bridge.py`). Sesli nota sesli cevap doner. Instagram linki tek seferlik hasat turu baslatir.

## Calistirma

`cp .env.example .env`, degerleri doldur, `./run.sh`. Kurallar ve Air ayrintisi: `.claude/CLAUDE.md`.
