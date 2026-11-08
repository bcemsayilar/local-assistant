# YouTube API uyumluluk denetimi formu taslağı

Form: https://support.google.com/youtube/contact/yt_api_form

Bulundu (parallaxtechnologies.net yayınlanmış gizlilik sayfalarından): Parallax Technologies LLC, 1111B S Governors Ave Ste 37573, Dover, DE 19904, United States, contact@parallaxtechnologies.net. Kişi adı: Burak Cem Sayılar (Google hesabında bu ad).

## Alanlar

- Sebep: yeni proje için denetim ve kota uzatma (yüklemelerin özel kilidinin kaldırılması)
- Başvuran: organizasyon, Parallax Technologies LLC
- Birincil web sitesi: https://parallaxtechnologies.net
- İletişim e-postası: me@cemsayilar.com
- API istemci adı: Parallax Uploader (adında YouTube geçmiyor)
- Birincil erişim URL: https://parallaxtechnologies.net
- Gizlilik politikası URL: https://parallaxtechnologies.net/privacy-policy
- Herkese açık mı: hayır, iç araç
- Proje numarası: 303715686259
- OAuth ile kullanıcı girişi: evet, yalnız iki kanal sahibi hesabı (kendi kanallarımız)
- Kullanım kategorisi: iç araç, yükleme otomasyonu
- Beklenen kullanım: günde birkaç video yükleme (videos.insert), arama yok
- Kota: varsayılan 10.000 birim yeterli, videos.insert günde en çok 5 çağrı

## Hizmet açıklaması (100 ile 5000 karakter)

Parallax Technologies LLC kendi sosyal medya kanallarına (YouTube @benburakcem ve @ailabturkey) kısa dikey videoları (Shorts) sıraya alıp otomatik yükleyen bir iç araç işletir. Araç yalnızca şirketin sahibi olduğu iki kanalın sahip hesaplarıyla OAuth 2.0 üzerinden yetkilendirilir, üçüncü taraf kullanıcıdan veri toplamaz, kullanıcı hesabı açmaz ve verileri satmaz ya da paylaşmaz. Kullanılan uç noktalar videos.insert (yükleme) ve channels.list (kanal doğrulama, mine=true). Yüklenen içerik kurucu tarafından üretilir ve onaylanır. Kitle genel YouTube izleyicisidir, gelir modeli kanal içeriğinin kendi markalarımıza ve ürünlerimize ilgi yaratmasıdır, API üzerinden reklam satışı yoktur.

## Kanıt olarak istenen

- Gizlilik politikası ekran görüntüsü ve ana sayfada gizlilik bağlantısını gösteren ekran görüntüsü
- OAuth izin ekranı ekran görüntüsü
- Yükleme betiği ya da ekran kaydı (iç araç için)
