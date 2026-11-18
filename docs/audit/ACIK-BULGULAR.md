# Açık bulgular sicili

**Kural (kurucu kararı 2026-11-10):** Bu sicil 2026-11-10'dan itibaren portföy denetimlerinin tek kaynağıdır. Kapanan madde buradan silinir; yeni denetim sonucu da buraya eklenir ve ham rapor tutulmaz. Eski ham raporlar (2026-11-05 denetim A, B, C ve temizlik kaydı; 2026-11-10 ana rapor, ek A ile F, 23 bulgu kapanışı) açık maddeleri buraya taşındıktan sonra silindi; kimlikleri "İlk görülme" satırında yalnız iz olarak duruyor.

**Nasıl güncellenir.** (1) Bir bulgu kapanınca maddenin tamamı silinir, "yapıldı" diye işaretlenmez; kurucu özetindeki sayılar ve elzem listesi aynı değişiklikte düzeltilir. (2) Yeni bulgu en sona sıradaki numarayla eklenir (numara yeniden kullanılmaz), alanlar aşağıdaki biçimde doldurulur, "İlk görülme" satırına tarih ve kaynak yazılır. (3) Bir denetim ajanı rapor dosyası yazmaz; bulgularını doğrudan bu dosyaya ekler, kapattıklarını siler. (4) Ölçüm tarihi değişen bir kanıt yeniden ölçülünce tarihiyle güncellenir. Son tam doğrulama: 2026-11-18, denetim kapanış ajanı (local-assistant görevlendirdi, kurucu brief'i onayladı): 33 maddenin her biri bugünkü durumla karşılaştırıldı; Mac Pro, Air SSH salt okuma, AWS ve ASC salt okuma. Kapanan ya da düzeltilen dört madde (S-41, S-43, S-53, S-70) silindi, kalan her maddeye "Durum 2026-11-18" satırı yazıldı.

Ciddiyet etkiye göredir: kritik (veri kaybı, sızıntı ya da servis durması riski), yüksek (yanlış işe, para kaybına ya da yanlış dış iletişime yol açabilir), orta (yanlış yönlendirme, ileride kırılma), düşük (düzen ve tutarlılık).

Madde biçimi: başlık satırında numara, ciddiyet ve tür (yarım iş, kopya, yanlış atıf, çelişki, verimsizlik, risk); altında Kanıt, Etki, Öneri, Kurucu kararı, İlk görülme.

## Kurucu özeti

**Kapsam (2026-11-16 gece denetimi, kurucu isteği: "sistemlerimizde herhangi bir inefficiency var mı, yarım kalan, duplike olan doküman, içerik, yanlış atıf").** parallax-content, project-benburakcem-ai ve çevresi, Mac Air ev sunucusu, mobil uygulama depoları, AWS ve yönetim depoları. cv-crafter ve WhatsappAgent kapsam dışı.

**Genel hüküm.** Kod ve git hijyeni iyi: hiçbir depoda izlenen video ya da ses yok, kasa kuralı tutuyor, 27 Air zamanlayıcısı belgeyle birebir, Syncthing çakışması yok, md dosyalarındaki 1.134 yol atfının yaklaşık yüzde 98'i canlı. Verimsizlik kodda değil, dört yerde toplanıyor:

1. **Okuma yükü.** Her oturum ve her alt ajan işe başlamadan önce çok büyük kural ve durum dosyaları okuyor: telefon-ajani.md 96 KB, reel-rehberi.md 154 KB, LESSONS.md 81 KB, her reel ajanına 91 ile 137 KB KURAL_PAKETI, app-fabrikasi STATUS.md 85 KB, dört yeni uygulamanın NEXT-SESSION dosyaları 19 ile 31 KB. Bir reel ajanı işe yaklaşık 120 bin token harcayarak başlıyor. Bu dosyaların içinde birbiriyle çelişen eski ve yeni kurallar var (S-44, S-56).
2. **Durumun tek yeri yok.** Aynı gerçeğin (bir uygulama reddedildi mi, bir reel yayınlandı mı, bir servis açık mı) üç ile beş dosyada elle tutulması, bir gün içinde ayrışıyor. 16 Kasım'da reddedilen beş uygulamanın depo notları "incelemede", yayınlanmış reel üç yerde "PARK", ev sunucusu belgesi n8n ve ağ için eski durumu yazıyor (S-45, S-59).
3. **Boşa ya da sağlıksız veriyle çalışan otomasyon.** Boş bir analiz raporu Clear Wave yayınını 18 Kasım'da durduracak; n8n'de çıktısı kimseye gitmeyen bir iş her hafta model çağırıyor; TikTok oturumu sessizce düşüyor; gece yedeğinin yaklaşık yüzde 80'i boş sayfa ve yeniden kurulabilir dosya (S-38, S-48, S-49, S-60).
4. **Tek kopya ve tek makine.** Üretim medyasının (29 GB) yedeği yok, Mac Pro diski yüzde 83 dolu ve Çöp 75 GB tutuyor; Air 16 Kasım'da voltaj hatasıyla plansız yeniden başladı ve canlı servisler tek o makinede (S-39, S-42, S-46).

**Bu gece kapatılanlar (sicile girmedi):** as-shot ve onscript push edildi, notları ve STATUS güncellendi (app-fabrikasi, local-assistant kararı); gece yedeği artık as-shot ve onscript git paketlerini alıyor, yeniden kurulabilir ios venv ve wda-build yedekten çıktı (local-assistant aa812ed); ev sunucusu belgesine VNC için SSH tüneli yolu yazıldı (80fdbba); ig-otomasyon'un yalnız DynamoDB'de duran 35 canlı kuralı dosyaya döküldü, git dışındaki beş kural dosyası commit'lendi, tabloda zaman içi kurtarma (PITR) açıldı, huni durumu iki belgede canlıya göre düzeltildi (ig-otomasyon 07de9c5); local-assistant TODO ve next-session'daki "incelemede" satırları düzeltildi.

**Sayılar (2026-11-18).** 28 açık bulgu: 4 yüksek (S-39, S-42, S-67, S-68), 22 orta (S-44 ile S-48, S-50 ile S-52, S-54 ile S-64, S-69, S-71, S-72), 2 düşük toplu (S-65, S-66). Kritik yok. 2026-11-18 kapanışında S-41, S-43, S-53, S-70 ve S-49 silindi. S-40 numarası gece içinde açılıp kapanan bir bulguya aitti (as-shot ve onscript yedeği), yeniden kullanılmaz.

**Elzem sıralama (etkiye göre):**
1. S-68: Air'de AWS yönetici anahtarı (`parallax-cli`) ve bütün SSM parametrelerini okuyan ops anahtarı, FileVault kapalı.
2. S-42: üretim medyasının yedeği (kurucu erteledi).
3. S-39: Air'in güç ve batarya kontrolü.
4. S-59: Air loglarında bot token'ı açık metin (mod 644).
5. S-67: dakikada bir tam tablo taraması; düzeltme dev dalında, deploy bekliyor.
6. S-64 ve S-54: açıkta duran ve ikilideki anahtarlar.
7. S-60: Clear Wave TikTok girişi düşük, kuyruk duruyor.
8. S-46: Mac Pro diski ve Çöp.

**Kurucu kararları (2026-11-17; soru dosyası cevaplar buraya işlenince silindi, tam metin git geçmişinde 699d853):**
1. S-38: kapandı (2026-11-17): boş toplama geçersiz sayılıyor, hata air-orkestrator'a istek olarak düşüyor, kapılar yalnız değerlendirmesi olan klasörü tur sayıyor, VidBerry kapısı olgun reel ve bekleyen kuyruk yokken analiz ve durdurmayı atlıyor. Gerçek bir hata gecesiyle henüz sınanmadı.
2. S-42: 29 GB üretim medyası incelensin, özellikle son bir ayda üretilenlerde yalnız final görsel, ses, video ve kapak kalsın, gerisi silinsin; kalan iCloud'a yedeklensin. İş içerik tarafının (self-branding). Kurucu 2026-11-17'de denetimi erteletti (acelesi yok), self-branding'den sonuç beklenmiyor.
3. S-39: Pillowtale ses sunucusu şimdilik Air'de kalır, ek yatırım yok. Plansız yeniden başlamanın sebebi Air'e bağlanan power bank, kurucu bir daha bağlamayacak.
4. S-46: boşalt. 2026-11-17'de Çöp'teki 14 günden eski öğeler silindi (yaklaşık 12,5 GB; Çöp 75 GB'tan 63 GB'a indi, kalanı 14 günden yeni). Kök sahipli `OneDrive.app` silinemedi, duruyor.
5. S-43, S-44: hayır, dosyalar küçültülmeyecek ve her seferinde okunacak. Yalnız birbiriyle çelişen ya da tekrar eden kurallar tekilleştirilsin. `telefon-ajani.md` 2026-11-17'de baştan sona okundu, çelişen satırlar güncel durumla işaretlendi (kural silinmedi, `.bak` kopyası Çöp'e); reel tarafı (S-44) self-branding'e devredildi.
7. S-54: aciliyeti yok, bekleyebilir (kurucu 2026-11-17).
8. S-66: needle, potty ve finance-agent 2026-11-17'de kapatıldı (silinmedi, `~/Mac-Projects/_arsiv/` altına taşındı; harita, app-registry ve OKU.txt güncellendi). Air'deki `~/Projects/finance-agent` ve `odysseus` klasörleri yerinde, silme kararı yok.
9. S-72: AWS kredisinin bitişi Ağustos 2028 (kurucu beyanı); bakiye hâlâ kayıtlı değil.

## Bulgular

### S-39 · yüksek · risk · Air plansız yeniden başladı, canlı servisler tek makinede
- Kanıt: Air `/Library/Logs/DiagnosticReports/ResetCounter-2026-11-16-012214.diag` "Boot faults: rst uv,vdd_boost_uvlo timeout"; batarya 838 döngü, yüzde 82; 01:10 TikTok yayın koşusu loga hiç düşmedi; 27 zamanlayıcı otomatik girişle geri geldi. Aynı gün pil yüzde 9'a kadar düşmüştü (local-assistant oturum kaydı, şarj izleme).
- Etki: canlı Pillowtale ses sunucusu, tünel, bot ve gece yayınları aynı makinede; güç sorunu tekrarlarsa hepsi birlikte durur.
- Öneri: adaptör, kablo ve bataryanın fiziksel kontrolü; canlı kullanıcıya hizmet veren servisin (Pillowtale ses) Air dışına alınması değerlendirilsin.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (Air ajanı).
- Durum 2026-11-18: Air 2026-11-16 01:22'den beri yeniden başlamadı (`last reboot`, yeni ResetCounter yok); 30 W adaptör bağlı, pil yüzde 80 ve şarj etmiyor, 838 döngü, kapasite yüzde 82, durum Normal. Pillowtale ASC'de hiç yayına girmedi (REJECTED) ve 2026-11-17'de kapandı, yani Air'deki ses sunucusunun canlı kullanıcısı yok. Takıldığı yer: fiziksel kontrol kurucuda. Sonraki adım: kurucu adaptörü ve kabloyu bir kez fiziksel kontrol eder; power bank bağlanmadan plansız açılış tekrarlamazsa madde kapanır.

### S-42 · yüksek · risk · Üretim medyası tek kopya, yedek yok
- Kanıt: Mac Pro `tmutil destinationinfo` "No destinations configured"; `project-benburakcem-ai` medyası Pro'da 29 GB, Air kopyası 0,9 GB (Air `.stignore` medyayı almıyor); `project-benburakcem-ai/CLAUDE.md:46` "assets-local Syncthing ile Air'de de" diyor, Air'de `assets-local/taban` 8 KB; `CLAUDE.md:91` "yedek durumu NEXT-SESSION'da" diyor, orada yok. Ham taban çekimleri iCloud'lu `Self Branding/b-roll/video` içinde, yayınlananların platform kopyası var.
- Etki: disk arızasında final reeller, klon ses verisi ve taban kopyaları gider.
- Öneri: yedek hedefi kararı; `CLAUDE.md` iki satırı düzeltilsin.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (benburakcem-ai ajanı).
- Durum 2026-11-18: değişmedi; `tmutil destinationinfo` "No destinations configured", Pro'da `posts/` 28 GB ve `assets-local/` 3,7 GB, `CLAUDE.md:46` ve `:91` satırları aynen duruyor. Takıldığı yer: kurucu erteledi, iş self-branding'in. Sonraki adım: kurucu inceleme ve iCloud yedeğini başlatınca self-branding iki CLAUDE.md satırını da aynı işte düzeltir.

### S-44 · orta · verimsizlik · Reel sisteminde zorunlu okuma yaklaşık 400 KB, kural paketi 14 kopya
- Kanıt: `project-benburakcem-ai/docs/reel-rehberi.md` 154 KB, `LESSONS.md` 81 KB (en yeni bölüm dosya sonunda), `adrien-tarzi.md` 58, `hikaye-insasi.md` 34, `adilet-animasyon-dili.md` 31, `cookbook.md` 23 KB; `kural_karti.py` hook'u her turda 8,7 KB ekliyor; her post klasöründe `KURAL_PAKETI.md` (14 kopya, 1,47 MB, 6 farklı içerik, üretici betik yok).
- Etki: her reel oturumu ve alt ajan işe başlamadan yaklaşık 120 bin token harcıyor; kopyalar ayrışıyor.
- Öneri: ölçüm raporları "gerekirse oku"ya alınsın; kural paketi tek betikle kaynaktan üretilsin, post'ta yalnız özet ve tarih kalsın.
- Kurucu kararı: evet (okuma sırası).
- İlk görülme: 2026-11-16 gece denetimi (benburakcem-ai ajanı).
- Durum 2026-11-18: kurucu kararıyla (2026-11-17) dosyalar küçültülmüyor, o kısım geçersiz; tekilleştirme kısmı açık: `KURAL_PAKETI.md` hâlâ 14 kopya ve 6 farklı içerik (md5), `reel-rehberi.md` 154 KB, `LESSONS.md` 81 KB. Takıldığı yer: self-branding alanı. Self-branding'e iletilecek: altı farklı kural paketi tek kaynaktan üretilsin ya da post klasöründe yalnız tarih ve atıf kalsın.

### S-45 · orta · çelişki · Durum dosyaları şişmiş ve bayat
- Kanıt: gift-almanac, beeward, printmargin, sunledge `docs/TODO.md` 5 satır, açık işler 19 ile 31 KB'lık günlük gibi tutulan NEXT-SESSION'larda; pillowtale NEXT-SESSION 32,8 KB ve coordinator 20,6 KB (kayıtların hepsi Eylül ve Ekim); watercleaner coordinator 22,6 KB; vidberry `CLAUDE.md` 25 KB ("assets-local ~4,8 GB" diyor, ölçüm 11 GB), `docs/TODO.md` 28 KB; `parallax-content/coordinator.md` 11 kaydın 6'sı kapanmış; eğitim reeli `POST.md:1`, NEXT-SESSION ve `data/reel-listesi.txt` içinde "PARK" ama 2026-11-16'da yayınlanmış (IG DfzcucmAZ0w); Edits MCP reeli yayınlanmış ama `POST.md:3` "TASLAK, YAYINLANMADI"; `project-benburakcem-ai/docs/TODO.md` #8 Meta başvurusunu "2026-10-20'den beri bekliyor" diyor (gerçek: red ve 2026-11-04 yeniden başvuru), #11 "karar konuşulmadan üretime geçilmez" dediği YouTube videosu üretimde; beeward ve printmargin "web sayfaları artık yanlış" notu (site 2026-11-12'de güncellendi); üç deponun `PARKED.md`'si "iCloud senkronu park" diyor, kodda CloudKit var.
- Etki: her oturum bayat satırları okur, yanlış işe başlama riski.
- Öneri: açık maddeler TODO'ya, NEXT-SESSION baştan yazılır kuralına dönüş; kapanmış kayıtlar silinsin.
- Kurucu kararı: sunledge eski maddeleri ve YouTube videosu için evet, kalanı hayır.
- İlk görülme: 2026-11-16 gece denetimi (dört ajan).
- Durum 2026-11-18: düzeltilenler: beeward web notu ve üç deponun kodda zaten olan iCloud park satırı silindi (beeward 72e8ba7, gift-almanac 9703b74, printmargin 363d3b2), vidberry `CLAUDE.md` assets-local 11 GB olarak düzeltildi (b25099b), kapanan beş uygulamanın NEXT-SESSION başına kapanış durumu yazıldı. Açık kalan: `project-benburakcem-ai/posts/2026-11-09_benburakcem-egitim-uc-hata/POST.md` hâlâ PARK, `2026-11-11_benburakcem-edits-mcp/POST.md` hâlâ TASLAK, `parallax-content/coordinator.md` 12 kayıt; watercleaner coordinator 22,8 KB ve vidberry `docs/TODO.md` 28 KB sahip oturumların. Takıldığı yer: self-branding alanı. Self-branding'e iletilecek: yayınlanmış eğitim ve Edits MCP reellerinin POST.md, NEXT-SESSION ve `data/reel-listesi.txt` durumları yayına çekilsin, coordinator'daki kapanmış kayıtlar silinsin.

### S-46 · orta · verimsizlik · Mac Pro diski yüzde 83, Çöp 75 GB, temizlik kuralı disk açmıyor
- Kanıt: `df` Data 733/926 GiB; `du ~/.Trash` 75 GB, 922 öğe (içerik temizlik artığı yaklaşık 15,6 GB, vidberry 27,6 GB, xcode 11,1 GB); yayınlanmış reellerde ara sürüm artığı yaklaşık 2,6 GB; `parallax-content/apps/vidberry` 8,6 GB, toplu temizlik onayı `vidberry/docs/TODO.md:164`'te 2026-10-13'ten beri açık; uygulama depolarında `build/` yaklaşık 6,1 GB, DerivedData 35 GB.
- Etki: "Çöp'e taşı" kuralı diski boşaltmıyor; disk dolarsa render ve build işleri durur.
- Öneri: 14 günden eski temizlik klasörleri boşaltılsın; yayınlanmış reel ara sürümleri kural yetkisiyle temizlensin; DerivedData için rutin.
- Kurucu kararı: evet (Çöp ve VidBerry listesi).
- İlk görülme: 2026-11-16 gece denetimi (benburakcem-ai, parallax-content ve mobil ajanları).
- Durum 2026-11-18: `df` Data 725/926 GiB (yüzde 82), Çöp 63 GB ve 357 öğe (14 günden eskiler 2026-11-17'de silindi), DerivedData 35 GB, yedi uygulama deposunda `build/` toplam yaklaşık 6,1 GB. Takıldığı yer: silme bu denetimin yetkisinde değil. Sonraki adım: kurucu Çöp'ün kalanı ve DerivedData için tek onay verir, local-assistant boşaltır. Güncelleme 2026-11-18 öğle: kurucu "Çöpü temizle" dedi, Çöp boşaltıldı (63 GB; üç kişisel öğe ve OneDrive.app bilerek bırakıldı), `df` Data 664/926 GiB (yüzde 75). Açık kalan: DerivedData 35 GB ve `build/` klasörleri, kurucu sözü bekliyor.

### S-47 · orta · çelişki · "Air'e medyasız" kuralı uygulanmıyor
- Kanıt: `home-server-syncthing.md` "683 MB" diyor; Air `~/Mac-Projects/parallax-content` 7,25 GB (500 KB üstü png 4,07 GB, 1.552 dosya; mp4 1,47 GB); Air `.stignore` 24 satır, görsel uzantısı yok; `shared/knowledge/app-store-header-motion/README.md:15` "_media Air'e gitmez" diyor, Air'de 403 MB.
- Etki: karar ile gerçek ayrışmış, Air'de gereksiz 4 GB üstü ve sürekli senkron.
- Öneri: `.stignore` belgedeki listeye hizalansın ya da belge düzeltilsin (air-orkestrator isteği).
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (Air ajanı); iz: S-01.
- Durum 2026-11-18: değişmedi; Air `parallax-content` 7,3 GB, Air `.stignore` 24 satır ve görsel deseni yok (yalnız mp4, mov, wav, mp3, m4a, webm), 500 KB üstü png ve jpg 1.796 dosya, `_media` 402 MB; `home-server-syncthing.md` ise png, jpg, jpeg, heic, webp, gif desenlerinin olduğunu ve Air kopyasının 683 MB olduğunu yazıyor. Takıldığı yer: Air değişikliği. Sonraki adım: air-orkestrator Air `.stignore`'a belgedeki görsel desenlerini ekler, tarama `needDeletes` 0 gösterince yok sayılan dosyaları siler ve belgedeki boyutu yeniden ölçer.

### S-48 · orta · verimsizlik · Gece yedeğinin büyük kısmı boş
- Kanıt: n8n `database.sqlite` 36.978 sayfanın 36.370'i boş (`PRAGMA freelist_count`); S3'te üç eski `app-fabrikasi` paketi 345 MiB; `git/` yolu süresiz saklanıyor. (ios venv ve wda-build 2026-11-16'da yedekten çıkarıldı.)
- Etki: günlük yedeğin çoğu israf.
- Öneri: n8n veritabanı `VACUUM`; S3'te eski paketler için yaşam döngüsü kuralı.
- Kurucu kararı: evet (S3 silme).
- İlk görülme: 2026-11-16 gece denetimi (Air ajanı).
- Durum 2026-11-18: değişmedi; n8n `database.sqlite` 36.978 sayfanın 36.357'si boş, S3 `git/app-fabrikasi/` altında üç eski paket (her biri 362 MB; 2026-11-06, 09, 11) duruyor; kovada `air/` için 35 gün, `git/` için yalnız eski sürüm 90 gün kuralı var. Takıldığı yer: Air (VACUUM) ve AWS yazma (yaşam döngüsü). Sonraki adım: air-orkestrator n8n durdurulmuşken `VACUUM` yapar; S3 kuralını local-assistant kurucu onayıyla ekler.

### S-50 · orta · kopya · Instagram yayını için dört ayrı yol
- Kanıt: `ig-otomasyon/tools/yayin.py` (SSM token), `project-benburakcem-ai/tools/instagram_yayinla.py` (kasa `meta`), `tools/instagram_karusel.py` (2026-11-12), `tools/instagram_karosel_yayinla.py` (2026-11-16, git dışı); son ikisi `CLAUDE.md`, `FILES.md` ve rehberde yok.
- Etki: yanlış token ya da hesapla yayın riski; kural yalnız birini bağlıyor.
- Öneri: tek yol seçilsin, diğerleri ona bağlansın.
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (benburakcem-ai ajanı).
- Durum 2026-11-18: değişmedi; dört yol da duruyor, `tools/instagram_karosel_yayinla.py` hâlâ git dışı, `instagram_karusel.py` ile birlikte `CLAUDE.md` ve `docs/FILES.md`'de anılmıyor. Hangisinin tek doğru yol olduğu kanıtla belirlenemedi, hiçbiri ölü kopya sayılmadı, taşıma yok. Takıldığı yer: self-branding (benburakcem-ai) tasarım kararı. Self-branding'e iletilecek: karusel için tek betik seçilsin, diğeri ona bağlansın ya da kaldırılsın, seçilen yol `CLAUDE.md`'ye yazılsın.

### S-51 · orta · kopya · Clear Wave analizi iki ayrışmış canlı kopya
- Kanıt: `apps/clearwave/tools/analiz/` ile `shared/analiz/` arasında `degerlendir.py` 7.358 ve 5.220 bayt, `kapi.py` 6.129 ve 4.831 bayt, 139 satır fark; iki ayrı zamanlayıcı (`clearwave-analiz` 02:00, `reel-analiz` 02:45).
- Etki: düzeltme yalnız bir kopyada kalıyor (S-38'in düzeltmesi iki yere yazılmak zorunda).
- Öneri: Clear Wave ortak servise geçsin ya da kopya resmen dondurulsun.
- Kurucu kararı: evet (watercleaner oturumu).
- İlk görülme: 2026-11-16 gece denetimi (parallax-content ajanı).
- Durum 2026-11-18: iki kopya da canlı (Air'de `com.parallax.clearwave-analiz` ve `com.parallax.reel-analiz` yüklü), `degerlendir.py` ve `kapi.py` arasında 227 satır fark; `shared/analiz/applar.json` notu Clear Wave ortak servise geçince kopyanın kaldırılacağını yazıyor. Ölü kopya yok, taşıma yapılmadı. Takıldığı yer: watercleaner oturumu ve Clear Wave'in bakım moduna geçişi. Sonraki adım: local-assistant Clear Wave'in son hata düzeltmesiyle ortak servise geçip geçmeyeceğine karar verir; geçmeyecekse `clearwave-analiz` kopyası resmen dondurulur.

### S-52 · orta · kopya · Uygulamalar arası elle tutulan kopya katmanlar
- Kanıt: gift, beeward, printmargin `web/*-terms.html` ile yayındaki site arasında 4 satır fark, dört uygulamanın `web/*-config-v1.json` dosyasında 18 satır eksik (paywall bloğu); altı uygulama ParallaxKit'e yerel yoldan bağlı, kit HEAD 0.1.1 etiketinin 5 commit ilerisinde ve etiketsiz, as-shot ve onscript 0.1.0'da; as-shot ve onscript'te 7 özdeş Swift dosyası, kaynak `app-fabrikasi/arastirma/asama3/ortak` ayrışmış; `asc_setup.py` dört depoda ayrı (105 ile 189 satır); paywall dört uygulamada kit'ten, yedisinde ayrı yazılmış; vidberry'de 25 üçüncü taraf `asc-*` skill ve brew `asc` (ikinci ASC zinciri).
- Etki: `web/` kopyasından yayın canlı hukuki metni eskiyle ezer; kit'teki her commit altı uygulamanın derlemesini değiştirir; her yeni uygulama kurulumu baştan yazılır.
- Öneri: `web/` kopyaları kaldırılsın; kit etiketlensin ve uygulamalar etikete bağlansın; tek yapılandırmalı ASC betiği.
- Kurucu kararı: ortak katman ve ASC betiği için evet.
- İlk görülme: 2026-11-16 gece denetimi (mobil uygulama ajanı).
- Durum 2026-11-18: beş uygulama kapandığı ve yeni uygulama açılmayacağı (kurucu kararı 2026-11-17) için `web/` kopyaları, `asc_setup.py` ve ortak paywall kısmı geçerliliğini yitirdi. Kalan tek canlı risk: Clear Wave `watercleaner/project.yml` ParallaxKit'e `path: ../parallax-kit` ile bağlı ve kit HEAD etiketsiz (`0.1.1-5-g9ecdf7f`). Takıldığı yer: watercleaner oturumu. Sonraki adım: Clear Wave'in son build'i kit `0.1.1` etiketine ya da o build'den önce atılacak yeni bir etikete sabitlenir.

### S-54 · orta · risk · Pillowtale TTS anahtarı ikiliye derleniyor, döndürmeme gerekçesi düştü
- Kanıt: `pillowtale/docs/TODO.md:26` ve `NEXT-SESSION.md:197` "incelemedeki build 8'de gömülü, döndürülemez"; build 2026-11-16'da reddedildi; anahtar `GeneratedSecrets.swift` ile derleniyor.
- Etki: ikilideki gizli anahtar, dayanağı kalmamış bir gerekçeyle döndürülmüyor.
- Öneri: anahtar döndürülsün ve sunucu tarafına alınsın.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (mobil uygulama ajanı).
- Durum 2026-11-18: anahtar hâlâ `GeneratedSecrets.swift` ile derleniyor (yalnız `TTS_API_KEY`); build 8 2026-11-16'da reddedildi, uygulama ASC'de hiç yayına girmedi ve 2026-11-17'de kapatıldı; `pillowtale/docs/TODO.md` notu bu bilgiyle güncellendi (95bb138), döndürme kuralına dokunulmadı. Takıldığı yer: kurucu (acil değil dedi). Sonraki adım: kurucu Air'deki ses sunucusunun kalıp kalmayacağına karar verir; kalırsa anahtar döndürülür, kapanırsa madde kapanır.

### S-55 · orta · verimsizlik · Dal düzeni karışık
- Kanıt: `project-benburakcem-ai` çalışma dalı `cloud/adilet-sov` (bir bulut pilotunun adı), `dev` 182 commit geride, yerel `main` ilk commit'te ve GitHub `main` ile ayrışmış, 6 yerel `claude/*` dalı içerilmiş; pillowtale'de 12 yerel `worktree-agent-*` dalı, ikisinde benzersiz 5 commit (a23837ac, a5347af6); watercleaner GitHub varsayılanı `clearwave-build` (2026-06-26, `dev` 185 commit ileride); potty varsayılanı `feat/review-prep`; vidberry `development` `main`'in 36 commit ilerisinde.
- Etki: hangi dalın güncel olduğu belgeden anlaşılmıyor; tek diskte yarım iş.
- Öneri: içerilmiş dallar silinsin, varsayılan dallar çevrilsin, pillowtale'deki iki dal incelensin.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (benburakcem-ai ve mobil ajanları).
- Durum 2026-11-18: pillowtale'de 12 `worktree-agent-*`, project-benburakcem-ai'de 6 `claude/*` dalı duruyor; watercleaner GitHub varsayılanı hâlâ `clearwave-build`; vidberry `development` `main`'in 40 commit ilerisinde. Takıldığı yer: dal silme ve varsayılan dal değiştirme bu denetimde yasak. Sonraki adım: local-assistant pillowtale'deki iki benzersiz dalı (a23837ac, a5347af6) inceledikten sonra içerilmiş dalların silme listesini kurucuya tek onayla sunar.

### S-56 · orta · çelişki · Orta CTA yasağı zorunlu okumadaki iki dosyada yok
- Kanıt: `reel-rehberi.md:130` ve `:533` "orta CTA yok (2026-11-08)"; `cookbook.md:60` "8 ile 10 sn orta CTA", `cookbook.md:136` ve `reel-rehberi.md:120` hâlâ orta CTA anlatıyor.
- Etki: ajan yasaklı kalıbı uygular.
- Öneri: üç yer rehbere hizalansın.
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (benburakcem-ai ajanı).
- Durum 2026-11-18: `reel-rehberi.md` hizalanmış (satır 77, 120, 130, 533 orta CTA yok diyor), ama `cookbook.md:60` hâlâ "8 ile 10 sn orta CTA (tek kelime)" diyor ve `:136` rehberin orta CTA'yı yorum kelimesi yaptığını yazıyor. Takıldığı yer: self-branding alanı. Self-branding'e iletilecek: `cookbook.md:60` ve `:136` 2026-11-08 kararına (CTA yalnız sonda) hizalansın.

### S-57 · orta · risk · Depolarda commit edilmemiş makine durumu ve gürültü
- Kanıt: `parallax-content` 80 commit edilmemiş değişiklik, 38'i Air zamanlayıcılarının ürettiği durum dosyaları (kuyruk json, tsv, jsonl, ledger), en eskisi 2026-11-11; `project-benburakcem-ai` 2.571 izlenmeyen dosyanın 1.831'i her kurgu klasörüne kopyalanan kütüphaneler (`three.min.js` 40 kopya, gsap 161 kopya, 373 ttf), gerçek değişiklik 29 dosya; `data/pvc-2026-11-14/secim` 171 MB `.npy` ignore'da değil.
- Etki: gerçek değişiklik gürültüde kayboluyor; `git add -A` depoyu yedi katına çıkarır.
- Öneri: makine durumu düzenli commit ya da `.gitignore`; kütüphaneler ortak klasörden; `.npy`, `*.log` ignore.
- Kurucu kararı: makine durumu için evet.
- İlk görülme: 2026-11-16 gece denetimi (parallax-content ve benburakcem-ai ajanları).
- Durum 2026-11-18: parallax-content'te 85 commit edilmemiş değişiklik (28'i kuyruk, tsv, jsonl, ledger, log türü makine durumu); project-benburakcem-ai'de 263 izlenmeyen giriş (alt dosyalarla 3.190), `data/pvc-2026-11-14/secim/*.npy` hâlâ ignore'da değil (`git check-ignore` boş). Takıldığı yer: iki depo self-branding'in. Self-branding'e iletilecek: makine durumu dosyaları ya düzenli commit'lensin ya `.gitignore`'a girsin; `.npy` ve `*.log` ignore edilsin.

### S-58 · orta · verimsizlik · Hasat notları sınırsız büyüyor
- Kanıt: `apps/self-branding/refs/buyume/` 541 KB (`format-referanslari.md` 210 KB), `shared/knowledge/hasat/` 170 KB, `kodla-tasarim/kaynak-notlari.md` 134 KB, `twitter/INDEX.md` 261 KB (852 kayıt), `ledger.md` 226 KB, `ig-temizlik/durum.jsonl` 154 KB; aynı kısa kod beş dosyada; `tetik-bekleyen.md` "Beklemede" 10 satır 2026-10-28'den beri donuk, "Satış" 42 satır; Twitter gece işi 7 koşunun 3'ünde 0 öğe işledi.
- Etki: okunamayacak boyutta ve tekrar eden kayıtlar; hasadın karara dönüştüğüne dair iz yok.
- Öneri: tekrarlı vakalar tek biçime; log dosyalarına döndürme; hasadın hangi kararı beslediği ölçülsün.
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (parallax-content ajanı).
- Durum 2026-11-18: değişmedi, büyüdü: `format-referanslari.md` 216 KB, `twitter/INDEX.md` 262 KB, `ledger.md` 234 KB. Takıldığı yer: self-branding alanı. Self-branding'e iletilecek: hasat kayıtlarına aylık döndürme ve hasadın hangi kararı beslediğinin ölçümü.

### S-59 · orta · çelişki · Ev sunucusu belgeleri gerçekle ayrışmış
- Kanıt: `home-server.md` ve `home-server-guvenlik.md` LAN ve Bonjour üzerinden VNC anlatıyor; 2026-11-16'da Pro'dan Air'e LAN'dan ulaşılamadı (evde iki ağ var), çalışan tek yol SSH tüneli. `home-server-guvenlik.md` "iproxy tüm arayüzlerde" (şimdi 127.0.0.1) ve "newsyslog conf yerinde" (2026-11-11'de kaldırılmış) diyor; `/usr/local/bin`'de üç `logkick-*` betiği duruyor; `home-server.md:111` olmayan `~/android-backup` yoluna atıf yapıyor. Air `~/Projects/local-assistant/logs/bot.log` ve `assistant.log` içinde bot token'ı açık metin (mod 644, Şubat 2026); `CLAUDE.md` "log boşaltıldı" diyor, bu yalnız `bot-stderr.log` için doğru.
- Etki: yanlış güvenlik tablosu; risk kabulü eksik bilgiyle verilmiş.
- Öneri: belgeler düzeltilsin; iki eski log silinsin.
- Kurucu kararı: evet (logların silinmesi).
- İlk görülme: 2026-11-16 gece denetimi (Air ajanı).
- Durum 2026-11-18: `home-server-guvenlik.md` düzeltildi (VNC LAN durumu, iproxy artık yalnız `127.0.0.1:18100` ve `:18101`, newsyslog dosyası kalkmış ve `com.apple.newsyslog` son çıkış 0; GAG ef4487b); `home-server.md` VNC bölümü SSH tünelini zaten yazıyor, `:111` `android-backup/` bir S3 öneki, ölü atıf değil. Açık kalan: Air `~/Projects/local-assistant/logs/bot.log` (1,35 MB, token desenli 9.230 satır) ve `assistant.log` (78 satır) mod 644 duruyor; `/usr/local/bin/logkick-*` üç betik duruyor ve hiçbir plist ya da newsyslog dosyası atıf vermiyor; `local-assistant/CLAUDE.md`'deki "log boşaltıldı" yalnız `bot-stderr.log` için doğru. Takıldığı yer: Air değişikliği. Sonraki adım: air-orkestrator iki eski logu siler ve `sudo rm /usr/local/bin/logkick-*` çalıştırır. Güncelleme 2026-11-18 öğle: air-orkestrator `bot.log` ve `assistant.log` dosyalarını boşaltıp 600 yaptı; logkick betiklerini hiçbir yer çağırmıyor, silmek sudo istiyor (kurucu).

### S-60 · orta · yarım iş · Clear Wave TikTok oturumu düşüyor
- Kanıt: Air `tiktok.log` 2026-11-12 01:10 ve 2026-11-16 03:10 "yükleme sayfası açılmadı ya da giriş yok"; zamanlayıcının son çıkış kodu 2; kuyrukta 4 bekleyen.
- Etki: TikTok kuyruğu sessizce geride kalıyor.
- Öneri: `watercleaner` Chrome profilinde giriş doğrulansın; giriş düşünce bildirim.
- Kurucu kararı: evet (giriş kurucunun).
- İlk görülme: 2026-11-16 gece denetimi (Air ve parallax-content ajanları).
- Durum 2026-11-18: hâlâ düşük; Air `tiktok.log` 2026-11-16 03:10, 2026-11-17 01:10 ve 03:10 aynı hata (giriş sayfasına yönleniyor, `2026-11-10_kombin-24-kova` bekliyor), zamanlayıcının son çıkış kodu 2. GAG `home-server.md`'deki commit edilmemiş 2026-11-17 notu SSH'tan başlatılan Chrome'un profil çerezlerini boşalttığını yazıyor, sebep bu olabilir (doğrulanmadı). Takıldığı yer: TikTok girişi kurucunun. Sonraki adım: kurucu Dock'taki watercleaner Chrome'unda TikTok `appclearwave` girişini yeniden yapar. Güncelleme 2026-11-18 öğle: son başarılı yayın 2026-11-15 03:10, oturum 2026-11-16'da düştü; 2026-11-18'den beri kuyruk ayrıca analiz kapısında duruyor ("uygulama.md yok"). Clear Wave bakıma alındığı için kurucuya yeniden giriş yerine zamanlayıcıyı kapatma soruldu.

### S-61 · orta · yarım iş · POST.md'siz ve haftalardır "onay bekliyor" klasörler
- Kanıt: `project-benburakcem-ai/posts/2026-11-11_benburakcem-fable-5-2` (1,08 GB, karusel yayınlanmış, kayıt yok), `2026-11-14_benburakcem-youtube-sirket-sistemi` (1,09 GB), `2026-11-06_motion-referans`, `2026-11-12_reelMotion-16-nvl72`; vidberry postlarında `2026-08-22_one-selfie-five-looks`, `2026-10-04_appstore-v6, v7, v8`, `2026-10-09_reel-01, reel-02`, `2026-10-25_kanca-testi`; pillowtale `2026-11-03_kanca-testi` (output boş); clearwave `2026-09-27_water-eject-15s`.
- Etki: hangi işin canlı olduğu belli değil.
- Öneri: her biri için kapat, sil ya da yeniden aç kararı.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (parallax-content ve benburakcem-ai ajanları).
- Durum 2026-11-18: değişmedi; benburakcem-ai'deki dört klasörde POST.md yok (fable-5-2, youtube-sirket-sistemi, motion-referans, reelMotion-16-nvl72). Takıldığı yer: self-branding alanı ve kurucu kararı. Self-branding'e iletilecek: listedeki her klasör için kapat, sil ya da yeniden aç kararını kurucuya tek listeyle sorsun.

### S-62 · orta · kopya · Anonim olmayan dans dosyaları üç yerde
- Kanıt: `apps/vidberry/refs/README.md` bu dosyaların yalnız `dans-non-anon/` altında durduğunu söylüyor; aynı videolar `dans-faceswap/kaynaklar/` ve `posts/2026-10-24_dans-faceswap-deneyi/inputs/kaynak/` altında da var (219 MB fazla).
- Etki: 2026-10-28 kurucu kararı (anonim olmayanlar ayrı saklanır) fiilen karşılanmıyor.
- Öneri: kopyalar tek yere indirilsin.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (parallax-content ajanı).
- Durum 2026-11-18: değişmedi; `refs/dans-non-anon` 106 MB, `refs/dans-faceswap/kaynaklar` 27 MB, `posts/2026-10-24_dans-faceswap-deneyi/inputs/kaynak` 58 MB. Takıldığı yer: self-branding (parallax-content içerik). Self-branding'e iletilecek: iki kopya `dans-non-anon/` altında teke indirilsin.

### S-63 · orta · risk · Self Branding arşivinde üretim çıktısı şüphesi (doğrulanmadı)
- Kanıt: `Self Branding/b-roll/video/2026-11-06_motion-broll.mp4`, `2026-11-07_isik-hikayesi-film-a.mp4` ve `-b.mp4` (141 MB): encoder Lavf, cihaz bilgisi yok; README bunları tarif etmiyor.
- Etki: "AI üretimi arşive yazılmaz" kuralı ihlal edilmiş olabilir.
- Öneri: menşei kurucuya sorulsun.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (benburakcem-ai ajanı).
- Durum 2026-11-18: üç dosya `Self Branding/b-roll/video/` altında duruyor, menşei sorulmadı. Takıldığı yer: kurucu cevabı. Self-branding'e iletilecek: üç dosyanın menşeini kurucuya sorsun, AI üretimiyse ilgili post klasörüne taşısın.

### S-64 · orta · risk · Kasada karşılığı olan eski anahtar dosyaları
- Kanıt: `local-assistant/finance_agent.env` (2026-03-07; değişken adları BINANCE_API_KEY, BINANCE_API_SECRET, GROQ, GROK, FINNHUB, N8N_API_KEY, TELEGRAM_BOT_TOKEN) ve kök `.env`; kasada park projeye ait dört `finance-agent--*` ve ölü `local-assistant--uygulama`, `mcp-obsidian--uygulama` girdileri; Air `~/.cache/air-backup` altında 435 MB şifresiz veritabanı kopyası; `parallax-cli` yönetici anahtarı 89 günlük; `parallax-content/.env` (2026-09-04'te vidberry'den kopyalanmış; değişken adları FAL_API_KEY, HIGSFIELD_API_KEY_MECEMSAYILAR, META_APP_ID, INSTAGRAM_APP_ID, IG_USER_ID), `shared/meta-api.md:44` hâlâ buna atıf yapıyor; ElevenLabs anahtarı üç yerde (kasada iki girdi ve proje `.env`), `seslendir.py` yalnız `.env` okuyor; Air'de mod 0644 `~/.env`, `~/Downloads/keys.txt` ve üç proje `.env` dosyası (içerik okunmadı); `GAG/service-access.md:25` kaldırılmış `~/.private_keys/asc/` yoluna atıf yapıyor.
- Etki: kasa kuralının dışında kalan kopyalar.
- Öneri: kasaya taşınıp dosyalar kaldırılsın, atıflar düzeltilsin.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (üç ajan).
- Durum 2026-11-18: değişmedi (içerik okunmadı); Mac Pro `local-assistant/finance_agent.env` ve kök `.env` (600), `parallax-content/.env` (600) duruyor ve `shared/meta-api.md:44` hâlâ ona atıf yapıyor; kasada dört `finance-agent--*`, `local-assistant--uygulama`, `mcp-obsidian--uygulama` ve iki ElevenLabs girdisi (`elevenlabs`, `project-benburakcem-ai--elevenlabs`); Air `~/.env` ve `~/Downloads/keys.txt` mod 644, üç proje `.env`'i (odysseus, finance-agent, cv-crafter-marketing) herkese okunur, `~/.cache/air-backup` 435 MB; `parallax-cli` anahtarı 91 günlük (2026-08-19). `service-access.md:25` atfı ölü değil, yolun artık olmadığını söylüyor. Takıldığı yer: anahtar taşıma, silme ve döndürme bu denetimde yasak. Sonraki adım: local-assistant kurucu onayıyla dosyaları kasaya taşıyıp kaldırır ve `parallax-cli` anahtarını döndürür (S-68 ile birlikte).

### S-65 · düşük · yanlış atıf · md dosyalarında ölü yol atıfları
- Kanıt: local-assistant betik taraması (2026-11-16): 1.134 yol atfından tarihçe dışı ölü olanlar: `parallax-site/README.md:39` (`~/Mac-Projects/vidberry/parallax-site/`), `vidberry/prompts/README.md:262` (`~/Desktop/vidberry-prompts/`), `GAG/third-party-agents.md:50` ve `:102` (`~/.local/lib/qwen-code/.../qc-helper/docs/`), `cemsayilar-site/CLAUDE.md:37` (CV dosya adı), `Data House/life/self-growth.md:514` (günlük dosyası yıl klasörüne taşınmış), `sunledge/CLAUDE.md:42` (Air'de olmayan kampanya klasörü), `printmargin/docs/NEXT-SESSION.md:93` (Air `printmargin-asc`), `pillowtale/docs/NEXT-SESSION.md:150`, `sunledge/docs/NEXT-SESSION.md:75`, `watercleaner/coordinator.md:67`, `vidberry/docs/features/background-change.md:183` (temizlenmiş masaüstü teslim dosyaları).
- Etki: düşük; atıfların yaklaşık yüzde 98'i canlı.
- Öneri: sahip oturumlar kendi dosyalarını düzeltsin.
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (local-assistant taraması).
- Durum 2026-11-18: düzeltildi: sunledge `CLAUDE.md` ve NEXT-SESSION (bbac32c), printmargin (363d3b2), pillowtale (95bb138), watercleaner (edff187), vidberry (ec6daac), cemsayilar-site (d34eb89); yanlış pozitif: `parallax-site/README.md:39` ve `vidberry/prompts/README.md:262` tarihçe cümlesi, `third-party-agents.md:50` ve `:102` Air yolları ve Air'de var. Açık kalan tek atıf: `Data House/life/self-growth.md:514` `~/ObsidianVault/gunluk/2026-10-09.md` (günlükler yıl klasörüne taşındı). Takıldığı yer: ObsidianVault bu denetime kapalı. Sonraki adım: local-assistant yolun `gunluk/2026/2026-10-09.md` olduğunu doğrulayıp satırı düzeltir.

### S-66 · düşük · toplu · Düzen ve tutarlılık
- Kanıt ve öneri, tek satırlar: Clear Wave takvimi "09:30 ve 20:00" diyor, zamanlayıcı 01:00 ve 03:00; `parallax-content/README.md` haritası 3 uygulama gösteriyor (gerçek 8) ve `shared/` altındaki dört klasörü anmıyor; `cw-dongu/` ve `kuyruk.py`'deki upload-post yolu ölü kod; `MODEL-PRICING.md:32` eskimiş; `marka/fontlar` klasöründe Playfair ve Inter yok; `metin_uret.py`, `bulut_ac.py`, `bulut_izle.py`, `qwen_uret.sh` kullanılmıyor; klon ses ara ürünleri 621 MB; cover-project belgesi bayat; Data House'ta 936 bölümün 28'inde yıl yok; Air'de iki log döndürücü (`log-dondur` 21 koşuda hiç döndürmedi); Air'de belgesiz Claude Desktop (11,1 GB, 8 GB bellekli makinede yaklaşık 350 MB); `parallax-site`'ta mağazada olmayan dört uygulama sitemap'te, `solledge.html` noindex değil; needle Eylül'den beri durmuş ve VidBerry'nin Mixpanel ve RevenueCat anahtarını kullanıyor; as-shot ve onscript `README.md`, `PARKED.md`, `coordinator.md` 0 bayt; potty `TODO.md` "v1.0 SHIPPED 2026-03-05" diyor, `CLAUDE.md` "hiç gönderilmedi"; Air'de ölü ağır klasörler (odysseus 547 MB, finance-agent 728 MB, belgesiz yaklaşık 1,6 GB).
- Kurucu kararı: durmuş projelerin kapatılması, log döndürücü ve Claude Desktop için evet.
- İlk görülme: 2026-11-16 gece denetimi (beş ajan).
- Durum 2026-11-18: kapanan alt maddeler: needle, potty ve finance-agent 2026-11-17'de arşive alındı. Ölçülen açıklar: Air'de iki log döndürücü hâlâ yüklü (`com.parallax.log-donus` ve `com.parallax.log-dondur`); Claude Desktop verisi `~/Library/Application Support/Claude` 12 GB; `parallax-site/sitemap.xml` kapanan beş uygulamanın ve Potty'nin sayfalarını listeliyor, `solledge.html` noindex değil; Air'de odysseus 547 MB ve finance-agent 728 MB (silme kararı yok). Diğer alt maddeler yeniden ölçülmedi. Takıldığı yer: Air, canlı site yayını ve self-branding dosyaları. Sonraki adım: air-orkestrator `com.parallax.log-dondur`'u kaldırır (kurucu kararı evet). Güncelleme 2026-11-18 öğle: kurucu kararı, kapanan uygulamaların sayfaları sitede ve site haritasında kalır (alt madde kapandı). İki log döndürücü için air-orkestrator'a `log-dondur` kaldırma isteği bırakıldı (20261118-111246).

### S-67 · yüksek · verimsizlik · ig-otomasyon dakikada bir tam tablo taraması yapıyor
- Kanıt: `ig-otomasyon/lambda/handler.py:618` `meta_items()` tabloyu baştan sona tarıyor (Scan); `retry_worker` dakikada bir, `reconcile_worker` on dakikada bir bunu çağırıyor; tablo 53.748 öğe, 5,5 MB; Cost Explorer Kasım 2026 (16 gün): okuma birimi 1,5515 USD, toplam kullanım 1,6893 USD (Ekim toplamı 0,2271 USD); 30 günde 88.991 Lambda çağrısının yaklaşık yarısı dakikalık iş.
- Etki: maliyet tabloyla birlikte büyüyor ve kredi bunu gizliyor; kredi bitince fatura olarak çıkar.
- Öneri: hesap listesi tek sabit öğeden okunsun (Scan yerine GetItem ya da Query).
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (AWS ajanı).
- Durum 2026-11-18: düzeltme yazıldı, deploy edilmedi: ig-otomasyon `dev` 48c7c8f (`meta_items` hesap listesini tek öğeden okur, liste yoksa ya da haftalık `refresh_tokens` çağırınca tarar ve listeyi yeniden yazar; `/callback` ve `oto.py hesap-ekle` listeye ekler). Yeni `tests/test_meta_index.py` 12 kontrolün 12'sini geçti (60 çağrıda tarama sıfır), mevcut beş test dosyası da geçti. Canlıda Scan sürüyor. Takıldığı yer: canlıya alma bu denetimin dışında. Sonraki adım: local-assistant `deploy.sh` ile dağıtır; ilk dakikalık koşudan sonra DynamoDB'de `pk INDEX` öğesini ve `retry_worker` loglarını, bir hafta sonra Cost Explorer okuma birimini kontrol eder.

### S-68 · yüksek · risk · Air'deki AWS anahtarı bütün gizli parametreleri okuyabiliyor
- Kanıt: IAM `ig-otomasyon-ops` politikasında `ssm:GetParameter` kaynağı `parameter/*`; SSM'de `/ig-otomasyon/anthropic-key`, `gemini-key`, `telegram-token`, `dash-secret` duruyor; README anahtarı "token okuma" diye tarif ediyor ve "S3 tmp yazma yetkisi yok" diyor, politikada `s3:PutObject tmp/*` var. Air'in diski şifresiz (FileVault kapalı).
- Etki: Air ele geçerse Anthropic, Gemini ve Telegram anahtarları okunur.
- Öneri: politika `/ig-otomasyon/token/*` ile sınırlansın (önce Air'de bu anahtarla başka parametre okuyan betik var mı bakılsın); README düzeltilsin.
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (AWS ajanı).
- Durum 2026-11-18: politika aynen duruyor (`SsmOkuma` kaynağı `arn:aws:ssm:*:573199225040:parameter/*`, yanında `GetParametersByPath`, `DescribeParameters`, S3 `tmp/*` için `PutObject` ve `GetObject`). SSM'de `anthropic-key`, `gemini-key`, `telegram-token`, `telegram-chat`, `dash-secret` ve üç `token/<hesap>` var. Air'in bu anahtarla gerçekten okuduğu: CloudTrail 2026-08-20'den beri `ig-otomasyon-ops` olaylarında yalnız `GetParameter /ig-otomasyon/token/17841422382755013` (102 kez) ve `/ig-otomasyon/token/17841448509552100` (18 kez), bir `DescribeParameters` (2026-10-23) ve bir `GetFunction` (2026-10-24) var; Air betiklerinde (`shared/analiz`, `marketing-agent/kampanyalar`, `ig-otomasyon/tools`, `android-agent/web`) adıyla anılan tek önek `/ig-otomasyon/token/`. Anahtar Air `~/Projects/marketing-agent/.env`, `OTO_CRED` ile `com.parallax.clearwave-reels`, `vidberry-reels`, `reel-analiz` ve `clearwave-analiz` kullanıyor. README düzeltildi (ig-otomasyon 48c7c8f). Daha büyük açık (yeni bulgu, bu maddeye bağlandı): Air kasasındaki `aws.env` yönetici kullanıcı `parallax-cli`'nin anahtarını taşıyor (anahtar kimliğinin son dört hanesi eşleşti, değer okunmadı), FileVault kapalı; bu anahtar Air'de durdukça dar politika Air ele geçince korumaz. Takıldığı yer: IAM yazma ve Air kasası bu denetimin dışında. Sonraki adım: local-assistant aşağıdaki taslağı kurucu onayıyla uygular ve Air'den yönetici anahtarının kaldırılmasını kurucuya sorar.
  - Taslak (yalnız SSM bölümü değişir, DynamoDB, logs ve S3 bölümleri aynen kalır): `SsmOkuma` ve `SsmListe` yerine tek ifade `{"Sid":"SsmTokenOkuma","Effect":"Allow","Action":["ssm:GetParameter","ssm:GetParameters"],"Resource":"arn:aws:ssm:eu-central-1:573199225040:parameter/ig-otomasyon/token/*"}`. `GetParametersByPath` ve `DescribeParameters` hiçbir Air betiğinde yok, düşer. Uygulama: önce `aws iam get-user-policy --user-name ig-otomasyon-ops --policy-name ig-otomasyon-ops` ile yedek, sonra `aws iam put-user-policy` ile yeni belge.
  - Test planı: (1) ops anahtarıyla (`OTO_CRED`) `/ig-otomasyon/token/17841422382755013` okunur, değer yazdırılmadan yalnız uzunluğu basılır; (2) aynı anahtarla `/ig-otomasyon/anthropic-key` ve `/ig-otomasyon/telegram-token` `AccessDeniedException` döner; (3) Air'de `~/Projects/ig-otomasyon/oto hesaplar` çalışır; (4) ertesi gece 01:00, 02:45 ve 03:00 işlerinin logları hatasız, CloudTrail'de `ig-otomasyon-ops` için `AccessDenied` yok; (5) sorun çıkarsa yedek belge aynı komutla geri yüklenir.

### S-69 · orta · verimsizlik · Yönetim oturumunun zorunlu okuması ve şişmiş iş listesi
- Kanıt: global CLAUDE.md 3.367 kelime (26,8 KB), proje CLAUDE.md 1.252, MEMORY 384, next-session 853, session-organization 2.178, agent-portability 1.087, home-server 2.505, telefon-ajani.md 11.244 kelime: toplam yaklaşık 22.900 kelime; `local-assistant/TODO.md` 38 KB, 46 açık madde (en uzunu 4.289 karakter), en az 10 madde başka oturumların işi; `next-session.md` "madde listesi değil" dediği halde TODO'daki 6 maddeyi tekrarlıyor; TODO'da sahibi ve tetiği olmayan 10 "araştırılacak" ve "tartışılacak" madde; `TODO.md:17` "Gemini kredisi bitik" notu 2026-11-15 commit'iyle (c3fd414) eskidi; `docs/development-log.md` son girdisi 2026-04-05; `CLAUDE.md` "Proje Yapisi" agentrun, bildirim, bin, tiktok-publisher ve tools klasörlerini saymıyor; MEMORY.md'de beş kayıt "Finance Agent" başlığı altında; başka dosyalarda sicilde olmayan S-06 ve S-34 atıfları.
- Etki: telefona dokunmayan oturum da 11 bin kelime okuyor; aynı iş iki yerde okunuyor; fikir maddeleri karara dönüşmeden birikiyor.
- Öneri: telefon-ajani.md yalnız telefon işine bağlansın (S-43 ile birlikte); TODO'da başkasının maddeleri sahibine verilsin; fikir maddeleri için tek karar: tarihli sahip ya da silme.
- Kurucu kararı: evet (2026-10-31 okuma kararı ve fikir maddeleri).
- İlk görülme: 2026-11-16 gece denetimi (AWS ve yönetim ajanı).
- Durum 2026-11-18: kurucu kararıyla (2026-11-17) zorunlu okuma dosyaları küçültülmüyor, o kısım geçersiz. Ölçülüp kapananlar: `TODO.md` 25 KB, Gemini satırı yok, `docs/development-log.md` 2026-11-16/17 girdisi var, MEMORY'de Finance Agent başlığı yok, sicil dışında S-06 ve S-34 atfı yok, `next-session.md` App Store satırı kapanış kararına göre düzeltildi (19a9c2a). Açık kalan: `CLAUDE.md` "Proje Yapisi" `agentrun/`, `bildirim/`, `bin/`, `tiktok-publisher/`, `tools/` klasörlerini saymıyor. Takıldığı yer: local-assistant'ın kendi CLAUDE.md'si (bu denetim CLAUDE.md'ye dokunmadı). Sonraki adım: local-assistant beş klasörü ve S-49'daki Ollama satırını tek değişiklikte CLAUDE.md'ye işler.

### S-71 · orta · yanlış atıf · ig-otomasyon belgeleri ve sistem şeması canlıdan geri
- Kanıt: `ig-otomasyon/README.md` "bellek 256 MB" diyor, `deploy.sh:46` ve canlı Lambda 512 MB; `docs/FILES.md` "tek Lambda, bağımlılık yok" diyor, iki Lambda ve Anthropic SDK var; Air yansısı 2026-11-10'dan (27 kural dosyası, Pro'da 38). `local-assistant/docs/sistem-semasi.html` başlığı ve son commit'i 2026-10-25; çizimde tiktok-publisher, DynamoDB, yedek kovaları, dashboard Lambda, huni ve `bin/mail` yok.
- Etki: marketing-agent eski kural kümesiyle çalışıyor; şema canlı sistemi göstermiyor.
- Öneri: belgeler güncellensin, Air yansısı yenilensin, şema yeniden çizilip yayınlansın.
- Kurucu kararı: hayır.
- İlk görülme: 2026-11-16 gece denetimi (AWS ve yönetim ajanı).
- Durum 2026-11-18: ig-otomasyon `README.md` (512 MB, Air anahtarının SSM ve S3 `tmp/` yetkisi) ve `docs/FILES.md` (iki Lambda, `huni.py`, anthropic SDK) düzeltildi (48c7c8f). Açık kalan: Air yansısı `~/Projects/ig-otomasyon` 2026-11-10'dan (27 kural dosyası, Pro'da 34) ve yeni `oto.py` oraya gitmedi; `docs/sistem-semasi.html` hâlâ 2026-10-25 tarihli. Takıldığı yer: Air'e kopyalama ve şemanın yeniden çizilip yayını (local-assistant). Sonraki adım: local-assistant S-67 dağıtımıyla birlikte Air yansısını tar kalıbıyla yeniler, ardından şemayı günceller.

### S-72 · orta · risk · AWS kredisinin durumu kayıtlı değil
- Kanıt: README ve CLAUDE.md "Activate kredisi" diyor; `service-access.md` yalnız 2026-08-19 başvurusunu ve ikinci reddi yazıyor; `freetier get-account-plan-state` hesap planı PAID, kalan kredi 0,0 USD; Cost Explorer Kasım kullanımını tümüyle karşılayan bir kredi satırı gösteriyor (-1,6893 USD).
- Etki: kredi bittiğinde fatura sessizce başlar (bugünkü tutar ayda birkaç dolar).
- Öneri: bakiye ve bitiş tarihi Billing sayfasından okunup belgelensin; aylık bütçe alarmı.
- Kurucu kararı: evet.
- İlk görülme: 2026-11-16 gece denetimi (AWS ve yönetim ajanı).
- Durum 2026-11-18: kredi durumu `service-access.md` "AWS Activate" altına yazıldı (GAG ef4487b): Cost Explorer Ekim ve Kasım 1 ile 17 arası kullanımın tamamını kredi satırıyla sıfırlıyor (Kasım 1,965 USD), bitiş Ağustos 2028 kurucu beyanı. Açık kalan: kalan bakiye API ile okunamıyor; bütçe `parallax-monthly-100` `IncludeCredit=true` ve ilk uyarı 50 USD, kredi bitince birkaç dolarlık fatura uyarı tetiklemez. Takıldığı yer: bakiye yalnız kurucunun konsolunda, bütçe değişikliği AWS yazma. Sonraki adım: kurucu Billing, Credits sayfasından bakiyeyi okuyup söyler; local-assistant aynı anda 5 USD ACTUAL eşikli ikinci bir uyarı kurar.
