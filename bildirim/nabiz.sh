#!/bin/bash
# nabiz.sh : Mac Pro -> Air nabzi. LaunchAgent com.local-assistant.nabiz 2 dakikada bir calistirir.
# Air'deki kurucuya_yaz.py bu nabza bakar: taze ve icinde bir yonetim oturumu varsa hata Telegram'a degil olay kaydina gider.
# Ayni turda Air'in olay kaydi Mac Pro'ya cekilir; air-olay-hook.sh yonetim oturumlarina yeni hata ve kararlari gosterir.
A=elifberraksayilar@100.108.136.36; S="ssh -o IdentitiesOnly=yes -i $HOME/.ssh/id_ed25519 -o ConnectTimeout=10 -o BatchMode=yes"
Y="$HOME/.local/share/bildirim"; mkdir -p "$Y"
# Claude Code surecinin komut adi surum numarasidir (or. 2.1.299); calisma klasorune gore yonetim oturumu sayilir
O=$(lsof -d cwd -Fcn 2>/dev/null | awk '/^c/{c=substr($0,2)} /^n/{if (c ~ /^[0-9]+\.[0-9]+\.[0-9]+$/) print substr($0,2)}' | sort -u)
L=""
echo "$O" | grep -qx "$HOME/Mac-Projects/local-assistant" && L="$L\"local-assistant\","
echo "$O" | grep -qx "$HOME/Desktop/Self Branding" && L="$L\"self-branding\","
printf '{"zaman": %s, "oturumlar": [%s]}\n' "$(date +%s)" "${L%,}" | $S $A 'cat > ~/Projects/local-assistant/bildirim/nabiz.json'
rsync -q -e "$S" "$A:Projects/local-assistant/bildirim/olaylar.jsonl" "$Y/air-olaylar.jsonl" 2>/dev/null
exit 0
