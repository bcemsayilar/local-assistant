# Next Session - Devir Notu (guncel: 2026-10-25)

Once `~/.claude/CLAUDE.md` (global kurallar, yonetim yapisi, telefon kurali), sonra `~/Desktop/Parallax Technologies LLC/General App Guidlines/session-organization.md` (roller; telefonlar orkestratorsuz, `kilit.py` ile dogrudan) ve `home-server.md`. Bir servise (AWS, Google Cloud, Supabase, Mixpanel vb.) dokunmadan once `~/Desktop/Parallax Technologies LLC/General App Guidlines/service-access.md`. Portfoyun semasi https://claude.ai/artifact/7RwAweEfyNQutzLT785WHY (kaynak `docs/sistem-semasi.html`, yapi degisince guncellenir). Acik isler `TODO.md`'de; bu dosya yalniz devir notu.

## Devam eden (2026-10-25 gece)

- **app-fabrikasi (Air, tmux + Remote Control):** pasaport ve teleprompter paralel; Kapı 2 kararları kurucudan geldi (ikisi birden, pasaportta önce regülasyon araştırması, fiyat rakiplerin ortası, Mixpanel, isimler için 3'er öneri). Sıradaki: aşama 3 kurulum (depo, commit), isimler için kurucuya 3'er öneri. Durum `~/Projects/app-fabrikasi/STATUS.md`, Kapı 2 özeti `arastirma/asama2/kapi2-ozet.md`. Bu oturumu local-assistant yönetir; mesaj SendMessage `app-fabrikasi` ile.
- **app-fabrikasi aşama 3 kararları (local-assistant kararı, 2026-10-25):** pasaport ilk sürüm ülkeleri ABD, GB, Japonya, Tayvan (AU şimdilik yok; DE, FR, CA kapalı; desteklenmeyen ülke dürüstçe "desteklenmiyor"). Fiyat kuralı rakiplerin en ucuzu ile en pahalısının ortası: pasaport tek seferlik $22.99, teleprompter yıllık ~$84.99 (kaydırma ve kayıt ücretsiz, ödeme ekranı kullanımdan önce çıkmaz). parallax-kit etiketli git bağımlılığı: `https://github.com/bcemsayilar/parallax-kit.git` `0.1.0` (özel depo; kit değişikliği gerekirse app-fabrikasi local-assistant'a yazar, yeni etiketi local-assistant atar). İsim kurucuda (Telegram'dan 3'er öneri gitti). Türkçe konuşma modeli ve Türkçe ses takibi ölçümü alt ajanda. app-fabrikasi ilk commit `e789f72`.
- **Yetki devri (global CLAUDE.md "Yetki devri"):** pillowtale ve app-fabrikasi kurucudan doğrudan teyit aldı (app-fabrikasi 2026-10-24 21:54 UTC, `af` ile). Eski açık oturumlar (vidberry-7f, clearwave, self-branding) bir kez teyit isteyebilir; yeniden açılan oturumlar kuralı başlangıçta yükler.
- **Telegram `af` köprüsü:** `assistant/integrations/oturum_kopru.py`; oturum boşalınca yazar, teslimi doğrular (2026-10-25 canlıda teslim doğrulandı). Teslimi kontrol: app-fabrikasi oturum kaydında `[Kurucu, Telegram'dan]` ile başlayan kullanıcı girdisi.
- **Bekleyen:** watercleaner Supabase geri açma (TODO), iPhone'larda klasörleme kurucuda.
- **Clear Wave kampanya linki:** provider ID 127767640 `app-registry.md`'de; biyografi `ct=clearwaveinstacmp202609`, DM kuralı `ct=clearwave_dm`.

## Kisisel / uyari

Kullanici sparring partner ister, kisa cevap ister. Urun adindan varsayma. Main'e commit icin acik izin gerekir (istisna: parallax-content). Geri donusu olmayan isler (unsend, silme, takipten cikma, rotate) once onay. Yetkili kimligin varken kurucuya "panelden bak" deme.
