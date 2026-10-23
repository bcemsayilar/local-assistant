#!/bin/bash
# air-cevap.sh <istek-adi> : air-orkestrator'un cevabini basar; henuz yoksa BEKLIYOR ve istegin durumunu yazar
N="$1"; ssh -o ConnectTimeout=10 -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 elifberraksayilar@100.108.136.36 \
  "D=~/Projects/air-orkestrator; if [ -f \$D/cevap/$N ]; then cat \$D/cevap/$N; elif [ -f \$D/istek/$N ]; then echo 'BEKLIYOR (kutuda)'; elif [ -f \$D/isleniyor/$N ]; then echo 'BEKLIYOR (isleniyor)'; else echo 'BULUNAMADI'; fi"
