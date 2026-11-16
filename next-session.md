# Next Session - Devir Notu (güncel: 2026-11-16 gece)

Önce `~/.claude/CLAUDE.md`, sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md`, `agent-portability.md` ve `home-server.md`; servise dokunmadan önce `service-access.md`. Sistem şeması https://claude.ai/artifact/7RwAweEfyNQutzLT785WHY (kaynak `docs/sistem-semasi.html`). Açık işler yalnız `TODO.md`'de; bu dosya yalnız devir ve doğrulanmış durum, madde listesi değil. Biten, doğrulanan ya da kurucunun kapattığı iş bu dosyadan ve TODO'dan sormadan kaldırılıp commit'lenir (global kural, kurucu kararı 2026-11-13).

## Durum (2026-11-13 doğrulandı)

- **Denetim defteri:** `docs/audit/ACIK-BULGULAR.md` boş. Ollama Air'de kurulu, modelsiz; kurucu Air'de bir model olmasını bekliyor, karar bekliyor. Doğrulamalar sırada: ig-otomasyon basış logu (S-06), cv-crafter blog workflow'u (aşağıda).
- **Bildirim modu `evde`.** `engel` her modda Telegram'a gider.
- **Mercury MCP** salt okuma, kullanıcı kapsamı. Güncel hesap Checking 5363 (Column N.A.); Wire Details PDF'i `~/Desktop/Parallax Technologies LLC/Finance/Mercury/` ("5363 YENİ"), eski 8385 ve 6712 kullanılmaz.
- **E-posta:** kalıcı araç `bin/mail` (gmail, is, yahoo; Proton yok), `bin/secrets run mail -- bin/mail ...`; KISITLI erişim, yalnız local-assistant okur, gönderme kurucu onayıyla (`GAG/service-access.md` "E-posta").
- **App Store:** As Shot (build 14) ve Onscript (build 8) 2026-11-13'te hâlâ Waiting for Review, inceleme notları "Hello, this is Burak..." biçiminde yüklü. Gönderim geri çekilirse abonelik ayrılır: grup sayfası Add for Review, abonelik sayfası Add for Review ve Draft Submission, sonra API ile sürümü ekle ve gönder. Header ve search videoları Asset Library'de hazır, 1.0 incelemeden geçince yerleştirilir. Pillowtale 2026-11-04'ten beri Waiting for Review (durum kontrol edilmedi). Dört yeni uygulama: TODO maddesi; TestFlight test ajanı 2026-11-13 akşam başladı, geçerse Gift Almanac ve Printmargin gönderilir.
- **ASC ikonları:** dört yeni uygulamada bağlı build ikonu depodaki yeni ikonla birebir (2026-11-13 indirip karşılaştırıldı); ASC web'de eski görünürse önbellek.
- **parallax-kit:** `ParallaxEyebrow` düz string literalini artık çevrilebilir anahtara gönderir (`@_disfavoredOverload`, 8286af5). Uygulamalardaki açık `LocalizedStringKey(...)` sarmalamaları zararsız, kaldırmak isteğe bağlı.
- **ig-otomasyon:** Motion kuralı (benburakcem) aktif. Başkasının yorumuna "gelmedi" diye cevap yazanlar tetiklemez, kendi yorumlarını yazmaları gerekir; kurucu elle DM gönderilmesini istemedi (2026-11-13 ensuysl).
- **Air TikTok:** `watercleaner` Chrome profilinde (appclearwave) TikTok girişinin yapıldığı 2026-11-11'den beri doğrulanmadı, 01:10 ve 03:10 yayınları bu girişe bağlı.
- **DM hunisi canlı (apple, hukuk):** bekçi Sonnet + Gemini (kendi projesi `gen-lang-client-0163841964`), Telegram'a olta, ciddi (kalıcı devir) ve sıcak (yalnız haber); tasarım `ig-otomasyon/docs/dm-ajani-tasarim.md`.
- **İşbirlikleri:** takip yeri `parallax-content/apps/self-branding/isbirlikleri/` (`2026-11-10_chatplace/`, `2026-11-10_eachlabs/2026-11-10_teklif-ve-sartlar.md`). ChatPlace: self-branding devraldı (2026-11-16), e-posta gönderimi local-assistant üzerinden. each::labs: 18 Kasım ortaklık duyurusu, karşı tarafın dönüşü bekleniyor.

- **Paywall standardı:** VidBerry ve Clear Wave kalıbı bütün uygulamalarda varsayılan (`GAG/design-language.md`), ortak bileşen parallax-kit `ParallaxPaywall`.
- **Ekran kaydı ve görüntüsü Mac Air'de** (parallax-content `CLAUDE.md`, 2026-11-15).

## Yarım kalan, söylenip yapılmayan, başlanıp bitmeyen (2026-11-16)

- **Gift Almanac ve Printmargin incelemede** (2026-11-15 21:15 UTC gönderildi, WAITING_FOR_REVIEW); sonuçtan sonra Beeward ve Solledge ikinci tur.
- **VidBerry Vibedesign reeli v2:** ajan aşama 1'de (metin, ElevenLabs sesi, Focusee düzeni ve dokunuş yakınlaşmalı montaj kodu). Çekim için iki şart: kurucunun arka plan seçimi (16 Focusee arka planı, numarayla) ve vidberry oturumunun kıyafet giydirme özelliği. Ajana "çekime başla" mesajı local-assistant'tan gider.
- **vidberry oturumu:** (1) kıyafet giydirme özelliği: kurucu tanımı "sahne ve poz verilir, referanstaki kıyafet o sahneye, poza ve mankene giydirilir; modelim var derse kendi modeli aktarılır". Önce mevcut akışlarda muadil taranacak (Virtual Model, On Model, choose-your-outfit), yeni şablon onun üstüne kurulacak; mağazaya (1.3.7) açma tarama sonucuna kadar bekliyor. Model Nano Banana 2 Lite (Google kendi API). (2) Gizlilik ve Şartlar sayfalarına Google Gemini ve Fal adıyla (uygulama içi onay ekranına dokunulmaz). (3) Ürünü 360 çevir: termos ya da parfüm şişesiyle kart görseli, PBR denemesi (fark yoksa kapalı, takıda açık, PBR'li kredi fiyatı yüksek), çeviriler, 1.3.8 build.
- **Maypop:** kit bağlantısıyla cevap gönderildi (2026-11-15 20:32 UTC, Air Chrome benburakcem), dönüş bekleniyor.
- **gcloud kalıcı oturum:** kurucu 2026-11-16 istedi; Workspace "Google Cloud session control" yeniden doğrulama politikası ve otomasyon için claude-ops servis hesabı yolu (bu oturumda başlatıldı, durumu aşağıda).
- **DM hunisi:** dışarıdan iş birliği ve satış teklifleri kuralda tanımsız (şimdilik ciddi sayılıp Telegram'a düşüyor), kurucu kararı yok; sıcak bildirimleri ilk günlerde elle oku.
- **Telefon betiği:** hesabın kendine attığı reellerin sohbetini gece turunda silme, yazılmadı.
- **Onscript:** Türkçe ses için yeni remote config anahtar adı app-fabrikasi'den bekleniyor.
- **iPhone 17 temizliği:** Fotoğraflar'da IMG_0108 ve IMG_0109, iCloud Downloads `elbise.jpg`, açık Safari sekmesi.
- **n8n CV-Crafter carousel:** Gemini anahtarının projesi faturalamadan çıkarıldı (ücretsiz katman); limit hatası verirse anahtar başka projeye alınır.

## Kurucuya sorulacak (TODO dışı)

- Masaüstündeki kalan gerçek dosyalar (metin dosyaları, ekran görüntüleri, `claude-basvuru/`): nereye.
- Global GSD kurulumu kaldırılsın mı (`~/.claude/settings.json` durum çubuğu ve güncelleme hook'u).
- Clear Wave CTA kararı; Air Chrome profilinde Coinbase ve Chrome Remote Desktop ne olacak.
- Önerilen küçük düzeltme: `twitter/gorev.md` giriş duvarında son satır `TWITTER DURDU` desin (self-branding'in dosyası).

## Başvuru bilgisi

- Air'de kurucu Chrome'unda (9223) ASC için yalnız ajanın kendi yeni sekmesi kullanılır (`home-server.md` istisnası); kurucu "Marka Chrome" klasörünü Dock'tan açıp girişleri kendisi yapar.
- Şirket telefonu: ABD numarası ve kurucunun TR numarası `~/Desktop/Parallax Technologies LLC/Şirket Adresleri.txt` sonunda; Apple ve benzeri formlarda şirket adına ABD numarası kullanılır.
- **n8n cv-crafter blog:** "CV-Crafter - Every 3 Days Blog Post Generator" (`zSJtI6YVAtveO3vF`) Groq düğümü 2026-11-11'de `contentType: raw` olarak düzeltildi. Doğrulama: `executions?workflowId=zSJtI6YVAtveO3vF` başarılı mı, Supabase'e yazdı mı. Aynı düğümde Groq anahtarı düz metin (kasaya ve n8n credential'ına taşınmalı, döndürme kurucu kararı). VidBerry Showcase workflow'ları 2026-11-09'dan beri kapalı, `home-server-servisler.md` satır 103 ve vidberry coordinator "ölü porta istek atıyor" notu bayat.
