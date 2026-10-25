#!/bin/bash
# air-olay-hook.sh : Claude Code UserPromptSubmit kancasi (Mac Pro). Yalniz yonetim oturumlarinda (local-assistant,
# Self Branding) Air'in olay kaydindaki yeni hata ve karar satirlarini bir kez baglama ekler. Kayit nabiz.sh ile cekilir.
case "$PWD" in
  "$HOME/Mac-Projects/local-assistant") ad=local-assistant ;;
  "$HOME/Desktop/Self Branding") ad=self-branding ;;
  *) exit 0 ;;
esac
Y="$HOME/.local/share/bildirim"; K="$Y/air-olaylar.jsonl"; M="$Y/gorulen-$ad"
[ -f "$K" ] || exit 0
n=$(wc -l < "$K"); g=$(cat "$M" 2>/dev/null || echo "$n")
[ "$g" -gt "$n" ] && g=0
yeni=$(tail -n +$((g + 1)) "$K" | /usr/bin/python3 -c '
import sys, json
for l in sys.stdin:
    try: d = json.loads(l)
    except ValueError: continue
    if d.get("seviye") in ("hata", "karar"):
        print("- %s [%s] %s%s" % (d["zaman"], d["kaynak"], d["metin"][:400].replace("\n", " "), " (Telegram gitti)" if d.get("telegram") else ""))')
echo "$n" > "$M"
[ -n "$yeni" ] && printf "Air olay kaydinda yeni hata ya da karar, sen bak:\n%s\n" "$yeni"
exit 0
