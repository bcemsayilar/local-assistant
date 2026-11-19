# Next Session - Devir Notu (güncel: 2026-11-19 öğleden sonra)

Önce `~/.claude/CLAUDE.md`, sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md`, `agent-portability.md` ve `home-server.md`; servise dokunmadan önce `service-access.md`. Sistem şeması https://claude.ai/artifact/7RwAweEfyNQutzLT785WHY (kaynak `docs/sistem-semasi.html`). Açık işler yalnız `TODO.md`'de; bu dosya devir ve doğrulanmış durumdur, madde listesi değil. Biten, doğrulanan ya da kurucunun kapattığı iş bu dosyadan ve TODO'dan sormadan kaldırılıp commit'lenir.

## Oturumun ilk işi

1. **Oturum kapanış komutu:** kurucu 2026-11-19'da istedi, taslak sıra `TODO.md` "Oturum kapanış komutu" maddesinde. Kural metni `GAG/session-organization.md`'ye yazılır, global `CLAUDE.md`'ye yalnız "oraya bak" satırı girer.
2. **Push bekleyen depolar (kurucu sözü yok, sor):** `local-assistant`, `cemsayilar-site`, `parallax-content`, `General App Guidlines`; `vidberry` development dalı da push'suz (vidberry oturumunun).
3. **Fal bakiye uyarısı** yarım kaldı (TODO maddesi); VidBerry'nin bütün üretimi Fal bakiyesine bağlı.

## Çalışma biçimi (kurucu düzeltmeleri, 2026-11-18 ve 19)

- Kurucu hedefi ve vizyonu koyar; planı, iş bölümünü ve diğer oturumlara giden brief'i local-assistant kurar. Kurucunun cümlesini ajana aynen aktarmak ve kapsamı sorulmayan yöne açmak yok (hafıza: `hedefi-plana-cevir-aktarma`). Örnek hata: "presetlerimiz iyi mi" sorusu kapak yenileme işine çevrildi.
- Cevaplar kısa; karar gerekmiyorsa sorma, sonuç getir. Kanıtsız iddia yok: bu oturumda üç iddia ölçümle düzeldi (VidBerry mağaza sürümü akışı, "kolye yok" bulgusu, manken kapakları).
- 5 USD ve üstü harcama kurucunun kendi sözüyle; altı local-assistant kararı.

## Doğrulanmış durum (2026-11-19)

- **ChatPlace:** reel yayında (https://www.instagram.com/reel/Df7AhUXEs7A/), otomasyon açık, test yorumunda yorum cevabı ve ilk DM geldi, ig-otomasyon çakışmadı, link Ecem'e gönderildi. ChatPlace araçları artık bağlayıcı olarak da var (`mcp__claude_ai_ChatPlace__*`).
- **Eğitim sayfası ve site:** `cemsayilar.com/egitim`, `/merhaba`, `/tr` yayında; `/api/ilgi` e-postaları Cloudflare KV `ILGI` alanına yazar (`cemsayilar-site/README.md`). Deploy `npx wrangler deploy`, anahtar `cemsayilar-site/CLAUDE.md`'deki komutla.
- **Stripe (Parallax):** tek etkin ürün atölye (`prod_VeNVz9TYYv1ezs`, 3.900 TL, ödeme linki `https://buy.stripe.com/eVqbJ2aSe0YuduAgTC5J606`), kapak ve marka ikonu yüklü, düğme siyah; altı CV Crafter ürünü arşivlendi. Hesap markalaması API'den değişmez, Air'deki admin Chrome profilinden (CDP 9306) yapıldı.
- **@benburakcem biyografisi:** Instagram, TikTok, YouTube'da "Claude Code / Yapay zeka ajanları / Gerçek projeler / Eğitim ve tüm linkler"; Instagram linki `cemsayilar.com/merhaba`. TikTok'ta link alanı yok (kişisel hesap, 362 takipçi).
- **VidBerry (vidberry oturumu yürütüyor):** durum `TODO.md` "VidBerry son test" maddesinin sonunda. Özet: Google yolları Fal'da, 100 kredi kayıt hediyesi, iade döngüsü koruması, yeni raflar canlı; style-shot ve üç yeni araç gizli, kurucu kararı bekliyor. Fal bakiyesi 19 Kasım'da yaklaşık 55 USD.
- **Google Gemini:** ön ödemeli bakiye bitti, bütün projeler 402; DM hunisi bekçisi Haiku yedeğinde. Kurucu kararı bekliyor (TODO maddesi).
- **IG sohbet temizliği:** 19 Kasım 04:00 turu bütün sohbetleri boşalttı. Elle başlatma: Air'de `launchctl kickstart gui/$(id -u)/com.parallax.ig-temizlik`.
- **Air ekran paylaşımı:** kalıcı SSH tüneli, `open vnc://elifberraksayilar@localhost:5901`.
- **AWS:** Air'de sınırlı `parallax-air` anahtarı; yönetici anahtar ve Stripe anahtarı yalnız Mac Pro'da (`bin/secrets sync-air` ikisini dışarıda bırakır).
- **E-posta:** `bin/secrets run mail -- bin/mail ...` (gmail, is, yahoo); gönderme `--kurucu-onayi` ile kurucunun sözü aynen. İş hesabı Gmail bağlayıcısından da okunur; ekli gönderimde `send_message` + `replyToMessageId` + `to`.
- **Bildirim modu `evde`.** `engel` her modda Telegram'a gider.

## Kurucudan beklenen kararlar

Hepsi `TODO.md`'de ilgili maddenin içinde; burada yalnız başlıklar: style-shot'un 1.3.7'ye açılması; çok planlı video zinciri; reelde gerçek marka adı; atölyenin beş adımı ve 90 dakika; üstü çizili 8.000 TL; kurum şeridi aralığı; `cv-crafter.com` kartı; DM hunisi bekçisinin modeli ya da Google yüklemesi; TikTok'ta işletme hesabına geçiş; push; SGK için CİMER metni hazırlansın mı; "reel dolu" sohbet hangisi.

## Cevap bekleyenler

Ecem (collab daveti teyidi, ödeme), Ömer (Firevibe: süre, tarih, brief), Maypop (fiyat teklifi), İspanya konsolosluğu vize şubesi, BLS ve SGK (19 Kasım hatırlatmaları), Anthropic destek (Max kredisi relink), Gökhan Sayılar (kurucu yazdı), each::labs, Meta App Review, TikTok Parallax Publisher, YouTube API denetimi, Onscript inceleme cevabı.

## Diğer oturumlarda açık duranlar

- **vidberry:** reel malzemesi self-branding'de; 1.3.8 işleri TODO'sunda; commit'ler development dalında, push yok.
- **self-branding ("Reel 12 v2 sonnet güncelleme"):** ChatPlace reel dosyaları commit'siz (`project-benburakcem-ai`, dal `cloud/adilet-sov`); VidBerry'nin "kendi referansını yükle" yönündeki iki reel taslağı; atölye duyuru içeriği ve kod kelimesi DM metni.
- **Başka oturumların commit'siz dosyaları:** `parallax-content` (`FORBIDDEN.md`, `coordinator.md`, telaffuz sözlüğü, Clear Wave rapor dosyaları), `cover-project/uretilen/2026-11-18_stripe-atolye/`.
- **VidBerry yayın kuyruğu boş:** 19 Kasım 06:00 yayını yapılmadı; yeni içerik vibedesign reeliyle gelecek.

## Önceki oturumlardan, bu oturumda doğrulanmadı

- App Store: Onscript ve As Shot'ta yalnız inceleme sonucu izlenir; kapanan uygulamalar TODO "Portföy kapanışı".
- Air TikTok: `watercleaner` profilinde `appclearwave` girişi kurucudan bekleniyor (Clear Wave kuyruğu maddesi).
- n8n CV-Crafter iş akışları kapalı; GCP `resume-ai-project-460420` anahtarları ve iki GitHub deposu kapanış listesinde.
- iPhone 17 temizliği: Fotoğraflar'da IMG_0108 ve IMG_0109, iCloud Downloads `elbise.jpg`, açık Safari sekmesi.
- Kurucuya sorulacaklar: masaüstündeki kalan gerçek dosyalar nereye; global GSD kurulumu kaldırılsın mı; Clear Wave CTA; Air Chrome profilinde Coinbase ve Chrome Remote Desktop.

## Başvuru bilgisi

- Mercury: salt okuma MCP; güncel hesap Checking 5363 (Column N.A.), Wire Details PDF'i `~/Desktop/Parallax Technologies LLC/Finance/Mercury/`.
- Şirket telefonu ve adresler: `~/Desktop/Parallax Technologies LLC/Şirket Adresleri.txt`.
- Air'de kurucu Chrome'unda (9223) yalnız ajanın kendi yeni sekmesi kullanılır; marka profilleri `~/android-agent/web/profil/profil.sh <ad> ac|kapat` (benburakcem 9302, vidberry 9304, admin 9306).
- Instagram web'de yorum Enter ile gitmez, "Post" düğmesine basılır; şablon düğmeleri (ChatPlace "Gönder") web DM'de görünmez. TikTok uygulaması açıkken telefon sürücüsü zaman aşımına düşer.
- SGK (İspanya işi): İstanbul Sosyal Güvenlik İl Müdürlüğü 0212 372 10 00; merkez Yurt Dışı İşlemleri Daire Başkanlığı 0312 458 77 99 (2020 tarihli genelgeden, güncelliği doğrulanmadı); ALO 170. Numaralar üçüncü taraf dizinlerinden.
