# LinkedIn Haftalik Post - Yazim Kurallari

Cem Sayilar'in haftalik AI bulten postlari icin tek kaynak yazim rehberi. Ornek postlar ayni workflow klasorunde: `../ornek-postlar.txt`.

## Dosya Akisi
- Uretim: 2026-08'den beri `~/Mac-Projects/newsletter-project` (LinkedIn teaser, metni OpenAI yazar, cikti `output/linkedin/<tarih>/`). Eski calisma taslagi `~/Desktop/linkedin-post.md` artik yok
- Arsiv + stil referansi: `~/Desktop/Self Branding/LinkedIn/linkedin-postlari.txt`
- Yeni post icin ayri md acilmaz.

---

## Format
- Acilis: 🏮 emoji ile basla, ardindan "Yapay zekada bu hafta one cikanlar:"
- Kapanis: "Bu haftalik benden bu kadar, keyifli bir hafta dilerim!" veya benzeri (kisaltilabilir)
- Hashtag'ler en sonda, 6-10 adet: #AI #YapayZeka #MachineLearning #LLM + konuya ozel

## Yapi
- Her haber maddesi bir emoji bullet ile baslar (🏮 🔬 🧠 🚨 💻 ⚡ 🌌 🛡️ 🔷 ⚫ 🧻 👨🏻‍🌾 🍎 🟣 🔵 🟢)
- Baslik satiri: emoji + kisa, net aciklama
- Alt detaylar: `>` isareti ile girintili satirlar
- Her madde 2-5 satir arasi, kisa ve oz
- Maddeler arasinda bos satir birak, nefes aldir
- Paragraflar arasi da bos satir, ozellikle uzun maddelerde alt konular arasinda
- Kaynak linkini maddenin sonuna ayri satirda ekle (`>` ile)

## Ton ve Dil
- Turkce yaz, teknik terimler Ingilizce kalsin (benchmark, inference, context window, MoE, open-weight)
- Konusma dili, samimi ama bilgili ton
- "biz" dili kullan, "siz" degil: "Beynimiz 20 watt harciyor" (dahil edici)
- Kisisel yorum kat: "benim en ilgimi ceken", "manidar :)", "bence"
- Kisisel yorum satirini ayri tut, maddenin icine gomme
- Rakamlar ve veriler kullan: yuzde, dolar, parametre sayisi
- Karsilastirmalar yap: "onceki X'e kiyasla Y kat daha iyi"
- Surpriz baglantilar kur: beklenmedik sektorlerden ornekler
- Kesin iddia/hukum yerine yumusak ifade:
  - YAPMA: "X bilim projesi finanse etmez, istihbarat finanse eder"
  - YAP: "X gecmiste istihbarat projelerini finanse etmekle biliniyor"
- Herkesin bilmeyebilecegi referanslara baglam ekle: "Doom (bir zamanlarin efsane oyunu)"

## Icerik Secimi
- Haftanin 5-8 onemli gelismesi (az ve oz)
- 1-2 tanesini derinlemesine ac (en ilginc/carpici olanlar)
- Mumkunse bolgesel cesitlilik: ABD, Cin, Avrupa, Ortadogu
- Sadece model/urun haberi degil: etik tartismalar, ekonomik etkiler, arastirmalar da
- Ayni sirketten birden fazla haber varsa en carpicisini sec
- Nis/dar teknik haberleri cikar (vLLM kernel update, Open WebUI terminal gibi)
- Genel okuyucunun ilgisini cekecekleri oncelikle: is piyasasi, buyuk yatirimlar, etik
- Capraz referans yap (gecen haftalara, ayni postta baska maddelere)
- Kaynak linkleri onemli haberlerin altina (Twitter, GitHub, Arxiv, sirket blog)

## LinkedIn Teknik Kisitlar
- `**` veya `*` markdown KULLANMA, LinkedIn desteklemiyor
- `#` baslik KULLANMA
- 1500-3000 karakter arasi ideal
- Emoji'ler dogal kullan, abartma
- "hashtag#" yerine dogrudan `#` kullan
- Sirket isimlerini LinkedIn'deki resmi isimleriyle yaz (tag'lenebilir olsun)

## Yapilmamasi Gerekenler
- Jenerik "AI cok gelisiyor" cumleleri yazma
- Her maddeyi ayni uzunlukta tutma, onemlileri ac digerleri kisa kalsin
- Sadece pozitif haber paylasma, elestirel bakis da olsun
- Link'leri cumle icine gomme, ayri satirda ver
- Halusinasyon yapma, emin olmadigin veriyi yazma
- Spekulatif/tahmin cumleleri ekleme: "Bu ucurum kapandikca sarsinti basliyor" gibi
- Ayni sirketten 2+ haber koyma, en guclusunu sec
- Dar teknik/nis haberleri koyma (hedef kitle genel AI takipcisi, ML muhendisi degil)

---

## Dikkat Edilmesi Gerekenler

> Gercek post duzeltmelerinden cikarilan dersler. Claude'un yazdigi taslak ile kullanicinin yayinladigi hali arasindaki farklar. Her yeni post oncesi oku.

### 2026-06-10 (Apple/Fable/MiniMax postu duzeltmeleri)

1. **Her habere kaynak linki ekle.** En tutarli fark buydu. Kullanici Fable, dark pattern ve Microsoft maddelerine `Haber -> URL` / `Detayli bilgi: URL` ekledi. Claude link koymamisti. Onemli her iddianin altina kaynak koy.

2. **Editoryal/hype baglaclarini at.** Kullanici sunlari sildi:
   - "Daha da ilginci:" (Apple maddesi)
   - "Elestirel not," (dark pattern basligi -> sadece "Dark pattern raporu")
   - "İste" (Fable detayi)
   - "Bir yandan da" (IPO satiri)

   Haberi dogrudan ver, suslemeden. Onem vurgusunu okur kendi yapsin.

3. **Zaman-bagimli kelime kullanma.** "bugun" silindi ("Anthropic bugun ... acti" -> "Anthropic ... duyurdu"). Post sonra okunabilir, tarihleyen kelimeler eskir.

4. **Mugla superlatif ve jargonu somutla.**
   - "premium" -> "piyasadaki en maliyetli model" (somut iddia)
   - "Geride kalan en buyuk bagimsiz agent lab" -> tamamen silindi (dogrulanamaz superlatif)

   Ingilizce gevsek sifat ("premium") yerine Turkce somut veri.

5. **"biz" kapsayici dil.** "paylasamadigim" -> "konusamadigimiz". Birinci tekil ("ben kacirdim") yerine cogul biz ("biz konusamadik"). Stil kuralinin canli ornegi.

6. **Baglami basliga parantezle koy.** "Cognition $1 milyar topladi" -> "Cognition (Devin'in gelistiricileri) $1 milyar topladi". Sirket/kisi kim oldugunu ilk satirda parantezle ver, okuru detay satirina birakma.

7. **Tek satir = tek iddia.** Claude uzun cok-cumleli `>` satirlari yazdi; kullanici bunlari boldu: baslik cumlesi ayri, her detay ayri `>` satiri. Microsoft ve Cognition maddeleri tek bloktan baslik + detay satirlarina ayristirildi.

8. **Kisisel renk/gozlem ekle.** Kullanici kendi gozlemlerini ekledi:
   - "AI kelimesi neredeyse her 3 dakikada bir soylendi" (Google I/O)
   - "Model duyurusunun Apple WWDC ile ayni gune gelmesi de dikkatimi cekti :)"

   `:)` kullanir. Claude'un kacirdigi sey: capraz-referans + kisisel gozlem.

9. **Kelime secimi - anlam karismasini onle.** "halka acilan ilk model" -> "genel kullanima acilan ilk model". "Halka acilmak" = IPO/borsa cagrisimi yapar, ayni maddede gercek IPO haberi varken karistirir. Kullanici bilerek netlestirdi.

10. **Kapanis kisaltilabilir.** Bu postta "Bu haftalik benden bu kadar, keyifli bir hafta dilerim!" -> sadece "Keyifli bir hafta dilerim!". Standart kapanis sart degil.
