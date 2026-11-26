# Next Session - Devir Notu (güncel: 2026-11-26 gece)

Önce `~/.claude/CLAUDE.md`, sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md`; servise dokunmadan önce `service-access.md`. Açık işler `TODO.md`'de, nihai hedef ve omurga günlüğü `OMURGA.md`'de; bu dosya devir ve doğrulanmış durumdur, madde listesi değil.

## Oturumun ilk işi

1. **ChatPlace karuseli 27 Kasım 10:00 yayını (self-branding devretti, kurucu onayları verildi):** yayın Mac Pro launchd `com.parallax.chatplace-karosel-yayin` ile çıkar (Mac Pro `caffeinate -ims` ile 10:30'a kadar uyanık; kapak kapanırsa uyur). Sıra: (1) `~/Mac-Projects/parallax-content/apps/self-branding/isbirlikleri/2026-11-10_chatplace/karosel_taslak/yayin/` altında `YAYINLANDI` var mı, `yayin_log.txt`'ten permalink ve media id; yoksa logdaki hata (hız sınırında betik kendisi bekler); (2) iPhone ile benburakcem'de gönderiyi düzenle, "Ücretli ortaklık" etiketini aç, iş ortağı chatplace.tr (kurucu: "beni bekleme, yayın çıktığında al telefonu yap benburakcemden"; API'den açılmıyor); (3) buraksayilar'dan CHATPLACE test yorumu at, DM ve 2711 linki gelsin (kurucu onayı verildi); (4) etiket açıldıktan sonra Ecem'e (is kutusu, uid 4292 thread'i) yayın linkini gönder (onay verildi); (5) kısa kodu `project-benburakcem-ai/docs/NEXT-SESSION.md` ChatPlace maddesine yaz; (6) `~/Library/LaunchAgents/com.parallax.chatplace-karosel-yayin.plist` kaldıysa çöpe taşı.
2. **Bekçinin ilk gerçek gecesi:** 27 Kasım 04:00 turu Air `~/android-agent/web/ig-temizlik.log`, bekçi `hasat-bekci.log`, orkestratör `~/Projects/air-orkestrator/cevap/` ve `kosu.log`. 17 Pro'nun yeni güç tuşu uyandırma yolunun ilk gecesi de bu (`wda.py` `pro_uyandir`, kayıtta "EKRAN UYANDIRILDI (guc tusu yolu)").
3. **Pomerol:** kurucu 27 Kasım'da ödemeyi yapacak (ihtiyaç kredisiyle); ödeme yapıldı deyince taslak `~/Desktop/İspanya/Yazismalar/pomerol-randevu-taslak-2026-11-26.txt` gmail'den uid 15400 thread'ine gider (görüşme önerisi: 28 Kasım Cumartesi 14:00 ya da 27 Kasım Cuma 16:00, İstanbul saati; girişimci izni sorusunun yazılı cevabı görüşmeden önce istenir).

## Doğrulanmış durum (2026-11-26)

- **Hasat bekçisi ve orkestratör:** Air `com.parallax.hasat-bekci` kayda her yazılışta (en sık 15 sn) ve 5 dakikada bir çalışır, sorunu `air-orkestrator/istek/`'e bırakıp orkestratörü hemen başlatır; orkestratör `parallax-content/shared/harvest/bekci/OYUN-KITABI.md` ve `DEGISIKLIKLER.md` ile kendisi çözer (değişiklik günlüğünü parallax-content ve local-assistant post-commit kancaları yazar). 26 Kasım'da uçtan uca denendi: istek 3 saniyede gitti, orkestratör 25 saniyede cevapladı, DNS önbellek sorununu bulup durdu (çözüm kitapta). Gizli kaos testi (Chrome çıkışı ve iPhone'u yeni gönderi ekranında bırakma): tur kendisi giriş yaptı (TOTP), hesap geçişleri tuttu, 5 öge geri alındı.
- **Telefonlar:** App Store otomatik güncellemesi iki telefonda kapalı (Instagram 17 Pro 456, iPhone 13 457). Otomatik kilit ikisinde Never. 17 Pro iOS 27.2.1: `/wda/lock`, `/wda/unlock` ve `/wda/locked` çalışmıyor; uyandırma ve karartma IOHID güç tuşu olayıyla (`wda.py` `pro_uyandir`, `kilit.py` `_pro_guc_kapat`), iki karanlık turda ilk denemede tuttu. Hesap listesi profil sekmesine basılı tutarak açılır, satır etiketi büyük küçük harf duyarsız eşleşir. Ayrıntı `telefon-ajani.md` 26 Kasım paragrafları; Air betik yedekleri `*.bak-2026-11-26`.
- **Hasat kuralı:** "kayıtlı" kontrolü yalnız `.md` notu sayar, ajan not bulamazsa soru sormadan yazar (DfSTjTjAeSH 3 Kasım referans indirmesi yüzünden kayıtlı sanılmıştı).
- **Claude anahtarı:** Parallax org kredisi 26 Kasım 13:25'te bitti (bu ayın Max kredisi eski Individual org'da kaldı, Anthropic destek gmail uid 15388); Air ajanı `CLAUDE_API_KEY_PERSONAL`'da (`agent.json.bak-2026-11-26`), deneme geçti. Abonelik yenilenince Parallax'a dönülür, yenileme günü kurucuya soruldu.
- **ChatPlace:** "CHATPLACE karusel 27 Kasım" otomasyonu açık (yorum ve DM, bütün postlar, takip kontrolü yok, 2711 linki, Gönder butonu doğrudan linke); ilk reelin "«CHATPLACE» to Direct or Comment" otomasyonu (1911) durduruldu, aynı kelimeyi iki otomasyon kullanamıyor. W-8BEN imzalı olarak Ecem'e gitti, ödeme süreci onlarda.
- **YouTube:** benburakcem yenileme anahtarı tam yönetim kapsamında (`shared/yayin-kuyrugu/youtube_yetki.py`), j2lS8lu2jaQ silindi. ailabturkey anahtarı hâlâ yalnız yükleme.
- **AWS önizleme:** self-branding'in S3 `parallax-onizleme-573199225040` ve CloudFront `dddoksnz5k1rc.cloudfront.net` kurulumu `service-access.md`'de.
- **VidBerry yayın kuyruğu:** kurucu kararıyla iş yok, Air `com.parallax.vidberry-reels` park edildi.

## Kurucu kararı bekleyenler

- Claude Max abonelik yenileme günü (Parallax org'a dönüş için).
- Geri alma ve sohbet silmeyi telefondan Chrome'a taşıma önerisi.

## Cevap beklenenler

Ecem (yayın sonrası), Pomerol (ödeme ve randevu), İstanbul Başkonsolosluğu vize şubesi (26 Kasım İngilizce hatırlatma), UGE (dört mail), BLS (tek soru: hangi liste esas), Nodisea, Gökhan abi, TikTok Publisher incelemesi.

## Diğer oturumlarda

- self-branding 26 Kasım gece kapandı; ChatPlace yayın sonrası işleri buraya devredildi (yukarıda). Atölye ve YouTube bölümleri onun `project-benburakcem-ai/docs/NEXT-SESSION.md` ve `docs/TODO.md`'sinde.
- vidberry: kendi `.env`'ini okuyan betikleri kasaya çevirme (`vidberry/coordinator.md` 2026-11-24).
