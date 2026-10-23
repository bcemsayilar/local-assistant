#!/bin/bash
# air-istek.sh <gonderen-oturum> <istek-metni | -> : Mac Pro'daki bir oturumdan air-orkestrator'a istek birakir, istek adini basar.
# Metinde ne, neden, hangi cihaz ya da servis, kurucu onayi var mi yazilir. Cevap: air-cevap.sh <istek-adi>
set -euo pipefail
FROM="$1"; shift; BODY="${1:--}"; [ "$BODY" = - ] && BODY=$(cat)
NAME="$(date +%Y%m%d-%H%M%S)-$(echo "$FROM" | tr -cd 'a-zA-Z0-9-').md"
printf 'Gonderen: %s\nTarih: %s\n\n%s\n' "$FROM" "$(date '+%Y-%m-%d %H:%M')" "$BODY" | \
  ssh -o ConnectTimeout=10 -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 elifberraksayilar@100.108.136.36 "cat > ~/Projects/air-orkestrator/istek/.$NAME && mv ~/Projects/air-orkestrator/istek/.$NAME ~/Projects/air-orkestrator/istek/$NAME"
echo "$NAME"
