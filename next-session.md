# Next Session - Devir Notu (güncel: 2026-11-25 gece)

Önce `~/.claude/CLAUDE.md`, sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md`; servise dokunmadan önce `service-access.md`. Açık işler `TODO.md`'de, nihai hedef ve omurga günlüğü `OMURGA.md`'de; bu dosya devir ve doğrulanmış durumdur, madde listesi değil.

## Oturumun ilk işi

1. **25 Kasım 04:00 gece turu:** Air `~/android-agent/web/ig-temizlik.log`. Bakılacaklar: `CHROME OTURUM` satırı (ilk kez çalışan otomatik giriş kontrolü), Opus düzeltmelerinin canlı ilk gecesi (tetik kuyruğu, karanlık ekran uyandırma, Unsend, huni sohbeti silme, iki tur eşiği), tur sonu kilit ve özet sayıları. Hata varsa `opus-analiz-2026-11-24.md` raporu bağlamdır.
2. **Avukat:** kurucu Sezen Türkkanlar'a LinkedIn'den yeniden yazdı; 25 Kasım sonuna kadar cevap yoksa Pomerol (150 EUR, ödeme bağlantısı mailde) ile devam.
3. **UGE:** 25 Kasım gece iki mail daha gitti (aynı thread: üçüncü hatırlatma ve kurucunun isteğiyle "URGENTE E IMPORTANTE"); ENISA 23 Kasım'da cevap vermişti, UGE hiç vermedi. Cevap gelene kadar UGE'ye yeni mail yok; gelmezse avukat üzerinden.
4. **İbrahim abi:** kurucu 25 Kasım akşamı LinkedIn'den yazacak (ABD saati).

## Doğrulanmış durum (2026-11-24)

- **Hasat:** Opus analizi ve üç canlı tam tur, son tur hatasız (parallax-content 9f6aeba, 522d826, 66bb12f, a350100). Huni sohbeti kapanınca silinir (benburakcem Chrome'dan, diğerleri telefondan), yorum Chrome arayüzünden (`yorum-ui.mjs`; eski web yorum ucu kalkmış), DM gelmeyen huni iki turda kapanır. Kurucu kararı: yoklayıcıya huni tetiklemesi yok.
- **Instagram girişi:** benburakcem TOTP kuruldu (kasa `instagram-totp`, `IG_TOTP_BENBURAKCEM`, Air'e senkron). Air `~/android-agent/sifre/ig-giris.mjs <hesap> [port] [--kontrol]` oturum düşerse şifre ve TOTP ile girer, 9302'de gerçek çıkıştan sonra denendi; gece turu 9223'te her tur çağırır. Kural `telefon-ajani.md` "Otomatik giriş betiği", global CLAUDE.md telefon satırı işaret ediyor. Diğer hesaplarda TOTP yok (kurucu: şimdilik benburakcem yeter).
- **iPhone 13:** iOS USB aksesuar ayarı ve tak-çıkar ile döndü; 24 Kasım'da iki kez USB'den düştü. uhubctl Air'deki hub'ı tanımadı. Düşerse telefon yeniden başlatma denenir (otomatik değil, hafıza `iphone-usb-dusunce-restart`).
- **DM hunisi:** "en çok nerede zorlanıyorsunuz" takip sorusu canlı (ig-otomasyon 860b695). Atölye sayfası ölçümü ve 45 saniye takip mesajı canlı (491d794, site 60bf26d), aydınlatma `cemsayilar.com/gizlilik/`; ilk gerçek veri görülmedi. Rapor `ig-otomasyon/tools/ek_rapor.py`.
- **DM kuralları:** ÖLÇÜM (DgHoHkekpsH) ve SİSTEM v2 PDF canlı; motion, fikir, sansursuz rehberleri Paylaşılan Drive'a taşındı (kurucu kararı: bütün kaynaklar yalnız "Parallax Rehberler" Paylaşılan Drive'ında).
- **Anahtarlar:** **26 Kasım 13:25 Parallax org kredisi bitti, API kapandı.** Sebep (Anthropic destek, 24 Kasım, gmail uid 15388): bu ayın Max API kredisi eski (Individual) org'a yüklenmişti, taşınmaz; Parallax org ilk kredisini abonelik yenilenince alır. Air dönünce yapılacak: `~/.config/parallax/agent.json` `claude_api_key_env` Individual org anahtarına geri çevrilir (`agent.json.bak-2026-11-24`), bir agentrun denemesiyle doğrulanır, abonelik yenilenince Parallax'a dönülür. Air dönünce ayrıca VidBerry yayın kuyruğu uyarısını üreten zamanlanmış iş kapatılır (kurucu 2026-11-26: kuyruk işi yok, VidBerry bireysel çalışıp atılıyor). Eski not: Air ajanı Parallax org anahtarında (`agent.json` `claude_api_key_env` `CLAUDE_API_KEY`), Max kredisi Parallax'a bağlandı (kurucu); Startups başvurusu Aralık ortası. Individual Org anahtarı `agentrun-air-personal-2` (süresiz) agent.env ve kasada duruyor. vidberry/.env okuyan başka depo betikleri kasaya geçti (watercleaner 5f883aa, vidberry bc29dfd, site 1e7de9b, ig-otomasyon 121f742); VidBerry'nin kendi deposundaki 15'ten fazla betik vidberry coordinator'da.
- **Gemini:** 1.000 TL'yi VidBerry görselleri bitirdi (16-19 Kasım, 132 çağrı); kurucu 250 TL yükledi, VidBerry tavanı 100 TL. Bekçinin Gemini katmanı döndü.

## Kurucu kararı bekleyenler


## Cevap beklenenler

Ecem (ChatPlace: karusel son hali 8 kare ve DocuSign imzası 25 Kasım'da bildirildi; Ecem 25 Kasım: W-8BEN ile devam ediliyor (Brex W-9 talebi önemsiz), karusel Ecem'in örnek postuna göre self-branding'de yeniden düzenleniyor; yayın 27 Kasım), Sezen Türkkanlar, UGE, Nodisea, Gökhan abi, TikTok Publisher incelemesi.

## 27 Kasım: ChatPlace karuseli

ChatPlace'te "CHATPLACE karusel 27 Kasım" otomasyonu duraklatılmış hazır (Gönder butonu, takip kontrolü, 5 soru, Ecem'in takipli linki utm 2711). Yayın kısa kodu gelince: yenisini karusele bağla ve aç; eski "«CHATPLACE» to Direct or Comment" otomasyonu bütün gönderilerde ve DM'de açık, onu yalnız Df7AhUXEs7A'ya bağla (DM tetiği o zaman kalkar). Ücretli ortaklık etiketi ve @chatplace.tr collab daveti self-branding'de.

## Diğer oturumlarda

- self-branding: atölye işi bütünüyle onda (kurucu kararı 2026-11-25, `project-benburakcem-ai/docs/TODO.md` "Atölye"); web sayfası ve DM otomasyonu isterse local-assistant yardım eder. Karta tıklayan 8 kişiye elle mesaj 25 Kasım'da gitti.

- self-branding: YouTube 1. ve 2. bölüm "-yoz" düzeltmesi ve render, 9 Aralık öncesi yayın, tek çağrı `/egitim`; duyuru reeli ve story (UYGULAMA kod kelimesi kuralı hazır ve kapalı, reel kısa kodu gelince local-assistant açar). Drive kuralı ve yeni linkler self-branding'e yazıldı (oturumu kapanmıştı, sonraki oturum `project-benburakcem-ai/docs/NEXT-SESSION.md` 3. maddesini silmeli).
- vidberry: kendi `.env`'ini okuyan betikleri kasaya çevirme (`vidberry/coordinator.md` 2026-11-24).
