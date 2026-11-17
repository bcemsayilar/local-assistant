#!/bin/bash
# ig-token-yenile.sh : kasadaki Instagram token'larini yeniler (60 gunluk), Air'e dagitir, vidberry/.env'deki ayni adli anahtarlari esitler.
# Zamanlayici: ~/Library/LaunchAgents/com.parallax.ig-token-yenile.plist (ayin 1'i ve 15'i 11:00). Deger hicbir yere yazdirilmaz.
S="$HOME/Mac-Projects/local-assistant/bin/secrets"
cd "$HOME/Mac-Projects/project-benburakcem-ai" || { echo "CD BASARISIZ"; exit 1; }
echo "== $(date '+%Y-%m-%d %H:%M') yenileme"
"$S" run meta -- python3 tools/ig_token_yenile.py || { echo "YENILEME HATASI"; exit 1; }
"$S" sync-air || echo "SYNC-AIR HATASI"
"$S" run meta -- python3 -I - <<'P'
import os, re
p = os.path.expanduser('~/Mac-Projects/vidberry/.env')
if os.path.exists(p):
    s = open(p).read(); n = 0
    for ad, v in os.environ.items():
        if ad.startswith('IG_ACCESS_TOKEN'):
            s2 = re.sub(r'(?m)^(%s=).*$' % re.escape(ad), lambda m: m.group(1) + v, s)
            if s2 != s: n += 1; s = s2
    open(p, 'w').write(s); print('vidberry/.env esitlenen anahtar:', n)
P
