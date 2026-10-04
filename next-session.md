# Next Session - Devir Notu (guncel: 2026-10-04)

Once `~/.claude/CLAUDE.md` (global kurallar, iki makine senkronu, tasima kurali, portfoy haritasi), sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/home-server.md` (Mac Air: servisler, izinler, iPhone, Syncthing) ve `app-registry.md` (hangi app hangi backend). Instagram islerinin kanonik dokumani `~/Desktop/parallax-content/shared/harvest/telefon-ajani.md`, islem kaydi ayni klasorde `ledger.md`. Bu dosya sadece acik isleri tutar; yapilanlarin ayrintisi o dokumanlarda. Onceki surum (2026-10-02 dogrulama listesi) tamamlandi ve kaldirildi.

## Durum (2026-10-04 sonu)

- Mac Air ve Mac Pro Syncthing ile senkron: Data House, parallax-content, Parallax Technologies LLC, ObsidianVault, `~/.claude/CLAUDE.md`. Git commit ve push sadece Mac Pro'dan.
- Telegram botu (`@burakcembot`) iki beyinli: duz metin lokal qwen, "claude" ile baslayan mesaj, gorsel, video, dosya ve sesli not Air'deki Claude Code'a gider. Ayrinti: `.claude/CLAUDE.md` "Claude kopru modu".
- Air'de iPhone 17 Pro (WDA, `ios-on.sh` / `ios-off.sh`), Android (adb), Safari ve Chrome Instagram araclari hazir.
- buraksayilar <-> benburakcem sohbeti 2026-10-03'te tamamen islendi (303 oge), mesajlarin neredeyse hepsi geri alindi. Kalan: benburakcem 4 (leoreal.ai, hesamious, byjoeym, dijitalakcin) ve 2026-10-04 eabhabranded (islendi, unsend onayi Telegram'da bekliyor), buraksayilar 2.
- finance-agent PARKED (servisler durduruldu, `~/Mac-Projects/finance-agent/PARKED.md`).

## Acik isler (oncelik sirasiyla)

1. **Anahtar sizintilari (kullanici karari):** Fal anahtari vidberry ve vidberry-ios git gecmisinde, rotate edilmeli. cv-crafter-marketing n8n dosyasinda Google anahtari. Air'deki 16 n8n workflow'unun 12'sinde anahtarlar dugumlere gomulu, n8n credentials'a tasinmali. Pillowtale uygulamaya gomulu anahtarlarla kendi oturumunda ilgileniyor. Ayrinti `app-registry.md` "Violations and gaps".
2. **Merkezi anahtar deposu kurulumu** (kullaniciyla konusuldu, karar bekliyor).
3. **Mac Pro Masaustu iCloud sorunu:** Masaustu iCloud dosya saglayicisina yarim bagli, parallax-content `.git` nesnelerinin bir kismi "dataless". Kullanici "Masaustu ve Belgeler"i kapatmali; sonra parallax-site ve (koordineli) parallax-kit `~/Mac-Projects`'e tasinacak. parallax-kit'i pillowtale ve watercleaner `../parallax-kit` ile kullaniyor, tek basina tasima derlemeyi bozar.
4. **local-assistant commit:** bot degisiklikleri, `claude_bridge.py`, `media.py`, `docs/` main'de commit bekliyor (onay gerekir).
5. **Telegram sesli cevap** (macOS `say`).
6. **Islenmemis sohbetler:** benburakcem <-> vid.berry, buraksayilar <-> cemworking2. Kullanicinin aradigi "marketing strateji" reel'i buraksayilar <-> benburakcem'de cikmadi, bu sohbetlerde olabilir.
7. **Mac Air hardening** (`TODO.md` ilgili bolum): FileVault karari, Tailscale ACL, misafir WiFi, log rotation.
8. **Syncthing surum farki:** Air 1.29.5, Mac Pro 2.0.11.

## Kisisel / uyari

Kullanici sparring partner ister, kisa cevap ister. Urun adindan varsayma. Main'e commit icin acik izin gerekir. Geri donusu olmayan isler (unsend, silme, takipten cikma, rotate) once onay.
