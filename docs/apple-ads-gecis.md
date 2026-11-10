# Apple Ads: Campaign Management API v5'ten Apple Ads Platform API'ye geçiş

Tek kaynak bu dosya. Hazırlayan: local-assistant alt ajanı, 2026-11-10, kurucu emri "todo elzemlerini yap" (local-assistant aracılığıyla). Canlı hesaba yalnız okuma çağrısı yapıldı; hiçbir kampanya, bütçe, anahtar kelime ya da negatif değiştirilmedi.

## Özet

- **Geçişin kendisi zaten yapılmış.** TODO maddesinin önermesi ("Air `asa_client.py` v5 kullanıyor") eski. Clear Wave'in `asa/` betikleri 2026-10-18'de, VidBerry'nin `scripts/asa_report.py`'si de ardından Apple Ads Platform API'ye (`https://api.ads.apple.com/v1`) taşındı. Mac Pro deposundaki `watercleaner/asa/*.py` ile Air'deki `~/Projects/watercleaner/asa/*.py` md5 ile birebir aynı (2026-11-10). Air'deki guard bu API ile çalışıyor; son log satırı ABD Exact kampanyasını 12,91 dolar harcama ve 10 kurulumla okuyor.
- **Portföyde v5 çağıran tek çalışan kod kalmadı.** `api.searchads.apple.com` yalnız şu yerlerde geçiyor: Air'deki yedek klasörü `~/Projects/watercleaner/asa-v5-backup-20261018/` (çalışmıyor, yalnız yedek), `watercleaner/asa/asa_client.py` ve `README.md` içinde tarihçe cümlesi olarak, VidBerry'nin eski bir planlama dokümanı (`docs/growth/asa-campaign-plan-feyzili-2026-09-06.md`) ve `General App Guidlines/app-registry.md` 26. satır (hâlâ "API v5" yazıyor, eski).
- **Aynı kimlik yetiyor, yeni kapsam ya da panel adımı gerekmiyor.** Kasadaki `apple-ads` servisiyle token alındı (`scope searchadsorg`), `GET /v1/acls`, `GET /v1/me`, kampanya sorgusu, kampanya raporu, Search Term Popularity ve Impression Share çağrılarının hepsi 200 döndü. Kurucunun Apple Ads panelinde yapacağı bir şey yok.
- **Yeni ve gerçekten işe yarayan kısım Insights.** Search Term Popularity ve Impression Share v5'te yoktu. İkisi için portföy geneli, salt okuma bir istemci yazıldı: `tools/asa/apple_ads_platform.py`.
- **Search Term Popularity'nin sınırı sert:** her ülke ve tür için tam 500 terim dönüyor (5000 istendi, 500 geldi). Bu bir "en çok aranan baş terimler" listesi; niş uzun kuyruk terimler (speaker cleaner, beekeeping, 3d print cost, balkonkraftwerk) içinde yok. Anahtar kelime keşfi için değil, kategori nabzı ve rakip markası bulmak için kullanılır.
- **Apple'ın son tarihi:** Campaign Management API v5 2027-01-26'da kapanıyor (Apple Ads Platform API Changelog sayfası ve v5 belge sayfasının uyarısı). Platform API sürüm 1.0, Ağustos 2026'da yayınlandı.

## Okunan kaynaklar

Yerel: `local-assistant/TODO.md` Apple Ads maddesi; `watercleaner/docs/TODO.md` (satır 20: "Apple Search Ads: closed. Campaigns stay as they are."), `docs/NEXT-SESSION.md` "Apple Search Ads" bölümü, `docs/DISCARDED.md` (ömür boyu bütçe reddi ve MUSIC kategorisi negatifleri); `watercleaner/asa/README.md` (v5'ten farkların tam listesi burada), `asa_client.py`, `spend_guard.py`, `search_terms.py`, `preload_negatives.py`, `create_us_campaigns.py`; Air'de `~/Projects/watercleaner/asa/` ve `asa-v5-backup-20261018/` (salt okuma, md5 ve grep); `vidberry/scripts/asa_report.py`; `General App Guidlines/service-access.md` (Apple Search Ads bölümü, zaten Platform API'yi anlatıyor), `secrets-management.md`, `spend-limits.md`, `app-registry.md`. `docs/marketing/master-brief.md` Apple Ads bölümü okunmadı, çünkü bu iş teknik geçişle ve keşif verisiyle sınırlı, kampanya stratejisine dokunmuyor.

Apple belgesi (developer.apple.com, belge JSON'u üzerinden okundu): [Apple Ads Platform API](https://developer.apple.com/documentation/apple-ads-platform-api), [Changelog](https://developer.apple.com/documentation/apple-ads-platform-api/changelog-apple-ads-platform-api), [Calling the Apple Ads Platform API](https://developer.apple.com/documentation/apple-ads-platform-api/calling-apple-ads-platform-api), [Implementing OAuth](https://developer.apple.com/documentation/apple-ads-platform-api/implementing-oauth-for-the-apple-ads-platform-api), [Applying Rate Limits](https://developer.apple.com/documentation/apple-ads-platform-api/rate-limits), [Managing Reports](https://developer.apple.com/documentation/apple-ads-platform-api/reports), [App Store Reports Endpoints](https://developer.apple.com/documentation/apple-ads-platform-api/apps-reports-endpoints), [Insights Endpoints](https://developer.apple.com/documentation/apple-ads-platform-api/insights-endpoints), [Search Term Popularity Query](https://developer.apple.com/documentation/apple-ads-platform-api/query-app-search-term-popularity-data), [Impression Share Query](https://developer.apple.com/documentation/apple-ads-platform-api/query-app-impression-share-data), [SearchTermPopularityTimeRange](https://developer.apple.com/documentation/apple-ads-platform-api/searchtermpopularitytimerange). Resmi bir uç nokta eşleme kılavuzu (migration guide) Apple'ın geliştirici belgesinde bulunamadı; basında anılan "Apple Ads Platform API Preview Release Notes" belgesi okunamadı. Aşağıdaki eşleme bu yüzden Apple belgesi artı canlı hesapta yapılan denemelerden çıkarıldı.

## API'nin temel farkları (belge ve canlı deneme)

| Konu | v5 | Platform API 1.0 | Kaynak |
| --- | --- | --- | --- |
| Taban URL | `https://api.searchads.apple.com/api/v5` | `https://api.ads.apple.com/v1` | belge, canlı |
| Kimlik | ES256 JWT client secret, `appleid.apple.com/auth/oauth2/token`, `client_credentials`, `scope searchadsorg` | aynı; client secret ömrü en fazla 180 gün, access token 3600 sn | belge, canlı |
| Bağlam başlığı | `X-AP-Context: orgId=...` | `X-AP-Context: adAccountId=...`; `/acls`, `/me`, `/orgs/{id}` için gerekmez | belge, canlı |
| Hesap modeli | org | org altında ad account; bizde 8847170 (bizim) ve 21669491 "Search Ads Basic" (bizim değil), roller `API Campaign Manager`, `API Conversions Sender` | canlı `/acls` |
| Okuma | `GET /campaigns?limit=` ve iç içe yollar | liste GET'i yok; her okuma `POST /v1/<varlık>/query` (`filters`, `sorting`, `pagination`); satırlar `result` altında düz liste | belge, canlı |
| Sayfalama | `limit`, `offset` | `pagination.offset`, `pageSize`; toplam yalnız `fetchTotalCount: true` ile gelir. Rapor ve Insights uç noktaları `fetchTotalCount`'ı 400 `REQUEST_UNRECOGNIZED_PROPERTY` ile reddeder (belgede yazmıyor, canlıda görüldü) | belge, canlı |
| Hiyerarşi | `/campaigns/{id}/adgroups/{id}/...` | varlıklar üst düzey, ilişki filtreyle (`adGroupId EQUALS`) | belge |
| Güncelleme | `{"campaign": {...}}` sarmalı | düz kısmi gövde; dizi alanı tamamen değiştirilir | belge, watercleaner README |
| Toplu işlem | `.../negativekeywords/bulk` | `POST /v1/<varlık>/bulk-create` gibi, `items: [{correlationId, data}]`, `allowPartialSuccess` | belge |
| Alan adları | `adamId`, `servingStatus`, `dailyBudgetAmount`, rapor `total`, `installs` | `promotedObjectId` (string), `systemStatus`, `dailyBudget.value`, `totalMetrics`, `tapInstalls`; sıfır metrik satırda hiç yok | watercleaner README, canlı |
| Hız sınırı | belgede sabit sayı | her yanıtta `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`; 429'da `Retry-After`. Ölçülen pencere: `/acls` 200, `/campaigns/query` 3000 (59 sn), kampanya raporu 200, Search Term Popularity 5 | belge, canlı |
| Yeni | yok | Insights (Search Term Popularity, Impression Share), Change History, Recommendations, Apple Maps reklamı (Brands) | belge |

## Bizim kodun kullandığı uç noktalar ve karşılıkları

Hepsi Platform API'ye zaten taşınmış durumda. "Eski" sütunu Air'deki v5 yedeğinden (`asa-v5-backup-20261018`), "Yeni" sütunu şu anki koddan.

| Betik ve kullanım | Eski (v5) | Yeni (Platform API, şu anki kod) | Durum ve fark |
| --- | --- | --- | --- |
| `asa_client.py` `clearwave_campaigns()` (guard, search_terms, preload_negatives, create_us_campaigns kullanır) | `GET /campaigns?limit=200`, istemci tarafında `adamId` süzme | `POST /campaigns/query`, `promotedObjectId EQUALS` filtresi, `fetchTotalCount` ile sayfalama | taşındı, canlıda 200 |
| `spend_guard.py` harcama okuma | `POST /reports/campaigns` | `POST /reports/apps/campaigns/query`, `timeRange`, `totalMetrics.localSpend`, `tapInstalls` | taşındı, Air'de çalışıyor |
| `spend_guard.py` tavanda duraklatma (YAZMA) | `PUT /campaigns/{id}` gövde `{"campaign":{"status":"PAUSED"}}` | `PUT /campaigns/{id}` gövde `{"status":"PAUSED"}` | taşındı; watercleaner README'ye göre 2026-10-18'de etkisiz duraklatmayla denendi. Bu çalışmada tekrar denenmedi (yazma yasak) |
| `search_terms.py` arama terimi raporu | `POST /reports/campaigns/{id}/searchterms` | `POST /reports/apps/searchterms/query`, `campaignId` filtresi zorunlu, `timeZone ORTZ` zorunlu | taşındı |
| `search_terms.py --negate` (YAZMA) | `POST /campaigns/{id}/adgroups/{gid}/negativekeywords/bulk` | `POST /negative-keywords/bulk-create`, kampanya düzeyi negatif | taşındı; v5'te reklam grubu düzeyiydi, şimdi kampanya düzeyi (Discovery tek reklam grubuyken eşdeğer) |
| `preload_negatives.py` | (v5 yedeğinde yok, sonradan yazıldı) | okuma `POST /negative-keywords/query` (`campaignId EQUALS` ve `adGroupId IS_NULL`), yazma `POST /negative-keywords/bulk-create` | baştan Platform API |
| `create_us_campaigns.py` | (v5 yedeğinde yok) | okuma `/adgroups/query`, `/keywords/query`, `/negative-keywords/query`; yazma `POST /campaigns`, `POST /adgroups`, `POST /keywords`, `POST /negative-keywords/bulk-create` | baştan Platform API; reklam grubu oluştururken `startTime` belgede isteğe bağlı görünse de zorunlu (watercleaner README) |
| VidBerry `scripts/asa_report.py` | v5 | `GET /acls`, `POST /campaigns/query`, `POST /reports/apps/campaigns/query` | taşındı (dosyanın kendi açıklamasına göre); bu çalışmada çalıştırılmadı |

Belirsiz kalan: (1) Apple'ın resmi eşleme kılavuzu okunamadı, yani v5'te olup Platform API'de bilerek kaldırılan bir uç nokta varsa burada görünmez; bizim kullandıklarımızın hepsinin karşılığı var. (2) AdServices atıf API'si (`AAAttribution`, `api-adservices.apple.com`; VidBerry `AttributionService.swift`, Clear Wave `Attribution.swift`) ayrı bir API; Apple'ın kapanış duyurusu yalnız Campaign Management API'yi anıyor, AdServices için bir kapanış ifadesi bulunamadı (güven: orta).

## Salt okuma doğrulaması (2026-11-10, canlı hesap)

Kimlik: kasadaki `apple-ads` servisi (`ASA_CLIENT_ID`, `ASA_TEAM_ID`, `ASA_KEY_ID`, `ASA_PRIVATE_KEY_PATH`), `bin/secrets run apple-ads` ile yüklendi; değerler yazdırılmadı.

| Çağrı | Sonuç |
| --- | --- |
| token, `scope searchadsorg` | 200, `expires_in 3600` |
| `GET /v1/acls` | 200; ad account 8847170 ve 21669491, roller `API Campaign Manager`, `API Conversions Sender` |
| `GET /v1/me` | 200; `orgId 8847170`, `userId 107020061` |
| `POST /v1/campaigns/query` | 200; 10 kampanya (Clear Wave 6, VidBerry 4). Yalnız iki ABD 2026-11 kampanyası ENABLED ve RUNNING (2145087086, 2145086150, bitiş 2026-11-15 20:00 UTC), geri kalan hepsi PAUSED |
| `POST /v1/reports/apps/campaigns/query` | 200; 10 satır, `EMPTY_METRICS` ile |
| `POST /v1/insights/apps/search-term-popularity/query` | 200; US ve TR, `PRODUCTIVITY_UTILITIES` ve `LIFESTYLE`, haftalık (2026-11-01 ile 07) ve aylık (2026-10) |
| `POST /v1/insights/apps/impression-share/query` | 200; Clear Wave US, 2026-11-02 ile 08, iki satır (ör. `airbuds` ve `noise app`, pay yüzde 1 ve 0, sıra 6) |

Gözlem, karar değil: Impression Share'in Clear Wave için döndürdüğü iki terim (`airbuds`, `noise app`) müzik ve ses yönlü; `asa/README.md`'deki "birincil kategori MUSIC, Search Match bunu okur" uyarısıyla tutarlı. Ayrıca Air guard logunda 2026-11-09 20:20 ve 20:40'ta Apple tarafında iki ardışık `500 Internal Server Error` var; guard üç ardışık hatada sessizce duraklatıyor, yani bir üçüncü 500 canlı kampanyayı durdururdu. Bu watercleaner oturumunun kararı.

## Search Term Popularity: ne veriyor, ne vermiyor

Belgeden: `POST /v1/insights/apps/search-term-popularity/query`; zorunlu `timeRange` (`start`, `end`, `granularity` `WEEKLY_SUN_SAT` ya da `MONTHLY`, saat dilimi UTC sabit); filtreler `countryOrRegion` (`EQUALS`, `IN`), `genre` (`EQUALS`, `IN`), `searchTerm` (`EQUALS`, `IN`, `CONTAINS`, `STARTS_WITH`, büyük küçük harf duyarsız), sayısal alanlar; isteğe bağlı `fields`: `rankInGenre`, `searchPopularityInGenre` (1 ile 100), `searchPopularity1to100` (ülkede bütün türler içinde), `searchPopularity1to5`. Haftalık veri her pazartesi 07:00 UTC'de önceki pazar cumartesi haftası için üretilir, 65 hafta saklanır; aylık veri her ayın 5'inde önceki ay için yenilenir, 15 ay saklanır. Sıralama alanı en fazla iki.

Tür listesi sabit 15 değer: BUSINESS, EDUCATION, ENTERTAINMENT, FINANCE, FOOD_DRINK, GAMES, HEALTH_FITNESS, LIFESTYLE, NEW_PUBLICATION, PHOTO_VIDEO, PRODUCTIVITY_UTILITIES, SHOPPING, SOCIAL_NETWORKING, SPORTS, TRAVEL. Utilities ayrı değil, Productivity ile birleşik; **MUSIC yok** (Clear Wave'in birincil kategorisi Music, yani Clear Wave'in kendi türünde bu rapor alınamaz, ikincil türü Utilities üzerinden `PRODUCTIVITY_UTILITIES` okunur).

Canlıda ölçülen sınırlar: her ülke ve tür için tam 500 satır (US PRODUCTIVITY_UTILITIES Ekim 2026'da en düşük `searchPopularity1to100` 59, TR LIFESTYLE'da 42); `fetchTotalCount` reddediliyor; hız sınırı penceresi 5 istek. Listenin tepesi markalar ve gezinme aramaları (chatgpt, vpn, google, pinterest, sahibinden).

İlk 30 terim (Ekim 2026, aylık, US ve TR, PRODUCTIVITY_UTILITIES ve LIFESTYLE; sıra, terim, popülerlik): `~/Mac-Projects/local-assistant/tools/asa/veri/stp-2026-10-US-TR-ilk30.tsv` (120 satır). Kısa görünüm:

- US PRODUCTIVITY_UTILITIES: chatgpt, vpn, google, gmail, chrome, gemini, duckduckgo, outlook, shadowrocket, google maps, claude ai, grok, chai, chat gpt, muse, claude, aptv, ai, waze, firefox ...
- TR PRODUCTIVITY_UTILITIES: vpn, chatgpt, google, gemini, türk telekom, gmail, chrome, getcontact, opera, claude, yandex, vpn iphone ... yapay zeka, otobüsüm nerede, authenticator, 1.1.1.1
- US LIFESTYLE: pinterest, zillow, ring, t-mobile, blink ... go wish (17), gowish (20), booksy, task rabbit, ecobee ...
- TR LIFESTYLE: pinterest, sahibinden, falcı bacı, doa, arabam.com, armut, kısmet, kahve falı, faladdin, fal ...

App'e özel `CONTAINS` denemeleri (Ekim 2026, aylık, bütün türler): Clear Wave için "water eject" yalnız TR ENTERTAINMENT'ta sıra 372 (popülerlik 51) çıktı, "speaker clean" ve "water remov" hiç yok. Gift Almanac için US SHOPPING'de "giftful" (sıra 50, popülerlik 69) ve "giftster" (413), US LIFESTYLE'da "birthday countdown" (367) ve ilk 30'da "go wish"; Türkçe "hediye" ve "doğum günü" yok. Beeward için arıcılıkla ilgili tek terim US BUSINESS "beekeeper" (412; bu muhtemelen arıcılık değil, aynı adlı bir iş uygulaması). Printmargin için ilgili terim yok ("filament" yalnız alakasız bir eşleşme). Solledge için DE PRODUCTIVITY_UTILITIES'te "fronius solar web" (487) ve "isolarcloud" (449), ikisi de inverter üreticisi uygulaması; "balkon" yok.

## Yeni istemci: yer, ad ve kapsam

Yer: `~/Mac-Projects/local-assistant/tools/asa/`. Gerekçe: `watercleaner/asa/` Clear Wave'e ait, Air kopyası canlı harcama guard'ını sürüyor ve zaten Platform API'de; oraya ikinci bir istemci koymak aynı işin iki kopyası olurdu ve Air'e kopyalama kuralını tetiklerdi. Insights verisi tek bir app'in değil bütün portföyün (Gift Almanac, Beeward, Printmargin, Solledge, VidBerry, Clear Wave), kasa ve servis erişimi de local-assistant'ın alanı. Ad: `apple_ads_platform.py`. Apple'ın yeni sürümü "v6" değil, Platform API 1.0 ve yol `/v1`; "v6" adı yanıltıcı olurdu.

- `tools/asa/apple_ads_platform.py`: salt okuma istemci. `call()` GET dışındaki her yöntemi ve sonu `/query` olmayan her POST'u ağa çıkmadan reddeder (`ReadOnlyError`). `asa_client.py` ile aynı imzalı `access_token()`, `call(method, path, **kw)`, `query(path, filters=(), what=None)`, `money()`; ek olarak `acls()`, `me()`, `campaigns(promoted_object_id=None)`, `campaign_report(start, end, ...)`, `search_term_popularity(countries, genres=None, granularity="MONTHLY", ...)`, `impression_share(promoted_object_ids, start, end, ...)`, `last_complete_week()`, `last_complete_month()`. `RateLimit-*` başlıklarına göre yavaşlar, 429'da `Retry-After` ile bekler. Kampanya duraklatma, oluşturma ve negatif yazma bilerek yok; onlar `watercleaner/asa`'da kalır.
- `tools/asa/test_apple_ads_platform.py`: çevrimdışı testler (yazma koruması, tarih yardımcıları) ve `--live` ile salt okuma testleri. 2026-11-10'da ikisi de geçti.
- `tools/asa/veri/stp-2026-10-US-TR-ilk30.tsv`: yukarıdaki ilk 30 listesi.

Kullanım:

```bash
cd ~/Mac-Projects/local-assistant
PY=~/Mac-Projects/watercleaner/asa/.venv/bin/python   # pyjwt, cryptography, requests burada var
$PY tools/asa/test_apple_ads_platform.py                                   # çevrimdışı
bin/secrets run apple-ads -- $PY tools/asa/test_apple_ads_platform.py --live
bin/secrets run apple-ads -- $PY tools/asa/apple_ads_platform.py stp --country US TR --genre LIFESTYLE --top 30 --out /tmp/x.tsv
bin/secrets run apple-ads -- $PY tools/asa/apple_ads_platform.py stp --country US DE --contains solar --top 50
bin/secrets run apple-ads -- $PY tools/asa/apple_ads_platform.py campaigns
```

v5 istemcisi (Air'deki yedek) silinmedi ve değiştirilmedi. `watercleaner/asa/` içindeki hiçbir dosyaya dokunulmadı.

## Search Term Popularity'yi yeni app'lerin anahtar kelime seçimine bağlama önerisi

Önce karşı görüş: bu rapor bizim app'lerimizin anahtar kelimesini seçmek için zayıf bir araç. Her ülke ve türde yalnız ilk 500 terim var ve ölçülen bütün niş terimlerimiz (speaker cleaner, beekeeping, 3d print cost, balkonkraftwerk, hediye) bu eşiğin altında kalıyor. "Bu terim listede yok" bilgisi tek başına "hacmi düşük" demek, sıfır demek değil; asıl hacmi ve rekabeti görmenin yolu hâlâ Apple Ads'in kendi keşif kampanyası ve Impression Share'in döndürdüğü `searchPopularity1to5` değeri.

Buna rağmen işe yarayan üç kullanım var:

1. **Rakip ve kategori lideri bulma.** Listenin tepesi markalardan oluşuyor; bu, kategoride kimin aranarak bulunduğunu gösterir. Gift Almanac için US'te "go wish", "giftful", "giftster" görünüyor: hediye ve dilek listesi kategorisinin aranan markaları bunlar. Market research kuralına (`General App Guidlines/market-research.md`) göre yorumları okunacak rakip listesi buradan beslenebilir. Solledge için DE'de "fronius solar web" ve "isolarcloud": balkon sistemi kullanıcısının zaten aradığı uygulamalar inverter uygulamaları; bu, Solledge'in ASO metninde ve ileride reklamda inverter markalarıyla ilişki kurmanın (uyumluluk dili, marka adını anahtar kelimede değil açıklamada) bir girdisi.
2. **Tür seçimi kontrolü.** Bir app'in birincil türü için `--contains` ile ilgili kelimenin hangi türde çıktığına bakılır. "water eject" TR'de ENTERTAINMENT'ta çıkıyor, Productivity Utilities'te değil; "birthday countdown" LIFESTYLE'da, "giftful" SHOPPING'de. Gift Almanac ASC'de Lifestyle (ikincil Productivity); birincil tür veriyle tutarlı, ikincil türün Shopping olması rakip markaların bulunduğu türle örtüşür, bu bir veri noktası.
3. **Dönemsellik.** Haftalık veri 65 hafta geriye gidiyor. Gift Almanac için Kasım ve Aralık haftalarında "gift", "christmas", "secret santa", "wishlist" terimlerinin ilk 500'e girip girmediği izlenebilir; girerse reklam ya da ASO güncellemesi zamanı odur.

Önerilen akış (sıra bağımlılığa göre): (a) her yeni app için birincil ve ikincil türü ve hedef ülkeleri belirle; (b) `stp --contains <çekirdek kelime>` ile bütün türlerde tara, çıkan markaları rakip listesine, çıkan türü tür kararına yaz; (c) çıkmayan niş kelimeler için ASO anahtar kelime alanını App Store Connect'in kendi önerileri ve rakip başlıklarıyla doldur, hacmi Search Term Popularity'den bekleme; (d) reklam açılırsa ilk haftadan sonra `impression_share()` ile terim başına `searchPopularity1to5` ve payımızı oku, bu niş terimlerin gerçek hacim göstergesi olur; (e) aylık veriyi her ayın 5'inden sonra çekip `tools/asa/veri/` altında sakla ki dönemsellik karşılaştırılabilsin.

## Kalan adımlar (öncelik sırasıyla)

1. **TODO maddesini düzelt:** "Air `asa_client.py` v5 kullanıyor" önermesi yanlış, geçiş 2026-10-18'de yapıldı. Madde, "Search Term Popularity'yi app'lerin anahtar kelime ve tür kararına bağla" ve "v5 yedeğini kaldır" olarak daraltılabilir. Kurucu onayıyla.
2. **`General App Guidlines/app-registry.md` 26. satırı güncelle:** hâlâ "API v5 `https://api.searchads.apple.com/api/v5/`" yazıyor; doğrusu Platform API, `https://api.ads.apple.com/v1`, ad account 8847170 (ayrıntı `service-access.md`).
3. **`watercleaner/asa/README.md`'deki "VidBerry'nin `scripts/asa_report.py`'si de aynı taşımaya ihtiyaç duyuyor" cümlesi eski,** dosya taşınmış. watercleaner oturumuna bildirilir.
4. **Guard'ın Apple 500'üne dayanıklılığı:** 2026-11-09'da iki ardışık 500 görüldü; üç ardışık hata canlı kampanyayı sessizce duraklatır. Tavan korumasını gevşetmeden geçici 500'ü ayırmak watercleaner oturumunun kararı.
5. **v5 yedeğini kaldır:** Air `~/Projects/watercleaner/asa-v5-backup-20261018/` artık çalışmayan bir API'yi çağırıyor; Apple'ın 2027-01-26 kapanışından sonra hiçbir değeri kalmaz. Air değişikliği olduğu için air-orkestrator'a istek olarak ve kurucu onayıyla. `asa_client.py` içindeki tarihçe cümleleri kalabilir.
6. **Yeni app'ler için ilk tarama:** Gift Almanac, Beeward, Printmargin, Solledge için yukarıdaki akışın (b) adımı. Bu belge yalnız ilk denemeyi içeriyor.

## Kurucuya sorular

1. TODO'daki Apple Ads maddesi "geçiş yapıldı" diye daraltılsın mı, yoksa Search Term Popularity ve yedek temizliği ayrı iki madde mi olsun?
2. Search Term Popularity verisi aylık olarak düzenli çekilip saklansın mı (Air'de zamanlayıcı gerektirir, air-orkestrator işi), yoksa yalnız app kararı anında elle mi kullanılsın?
3. Gift Almanac ASC'de Lifestyle (ikincil Productivity) olarak ayarlı. Veride aranan rakip markalardan "go wish" ve "birthday countdown" LIFESTYLE'da, "giftful" ve "giftster" SHOPPING'de çıkıyor. İkincil tür Productivity yerine Shopping olsun mu? (Yalnız ikincil tür, birincil Lifestyle veriyle tutarlı.)
