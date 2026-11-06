#!/bin/bash
# backup-air.sh : Air'deki yalniz Air'de bulunan verinin sifreli (age) ve versiyonlu (S3) yedegi. Air'de calisir (LaunchAgent com.parallax.air-backup, gunde bir, 03:30).
# Ozel anahtar Air'de YOKTUR, yalniz herkese acik anahtar var; geri acma Mac Pro'da. Rehber: General App Guidlines/home-server.md "Air yedegi".
set -u
export PATH=/opt/homebrew/bin:$PATH
H="$HOME"; D=$(date +%Y-%m-%d); LOG="$H/android-agent/web/backup-air.log"; CACHE="$H/.cache/air-backup"; W="$CACHE/$D"
B=parallax-air-backup-573199225040; R=eu-central-1
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }
set -a; . "$H/.config/parallax/secrets/aws-backup.env"; . "$H/.config/parallax/secrets/backup.env"; set +a
AK="${AIR_BACKUP_AWS_ACCESS_KEY_ID:-}"; SK="${AIR_BACKUP_AWS_SECRET_ACCESS_KEY:-}"; PUB="${AIR_BACKUP_AGE_PUBLIC_KEY:-}"
[ -n "$AK" ] && [ -n "$SK" ] && [ -n "$PUB" ] || { log "HATA anahtarlar eksik"; exit 2; }
command -v age >/dev/null || { log "HATA age yok"; exit 2; }
mkdir -p "$W/stage" || exit 2; umask 077
upload(){  # dosya anahtar
  curl -sS --fail --aws-sigv4 "aws:amz:$R:s3" --user "$AK:$SK" -H "x-amz-content-sha256: UNSIGNED-PAYLOAD" -T "$1" "https://$B.s3.$R.amazonaws.com/$2" >/dev/null 2>>"$LOG"
}
# 1) tutarli veritabani kopyalari
sqlite3 "$H/Projects/finance-tracker/finance.db" ".backup '$W/stage/finance.db'" 2>>"$LOG" || log "UYARI finance.db kopyasi alinamadi"
sqlite3 "$H/.n8n/database.sqlite" ".backup '$W/stage/n8n-database.sqlite'" 2>>"$LOG" || log "UYARI n8n veritabani kopyasi alinamadi"
# 2) dosya listesi (buyuk ve gereksizler disarida)
L="$W/list.txt"; : > "$L"
add(){ find "$@" -type f \( -size -20000k \) 2>/dev/null >> "$L"; }
cd "$H" || exit 2
find Projects/finance-tracker -type f -size -20000k -not -path "*/.venv/*" -not -path "*/__pycache__/*" -not -name "*.bak*" -not -name "dashboard.err" -not -name "dashboard.log" -not -name "finance.db" -not -name "finance.db-*" 2>/dev/null >> "$L"
find Projects/marketing-agent -type f -size -20000k -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/.venv/*" 2>/dev/null >> "$L"
( cd Projects/app-fabrikasi && git status --porcelain 2>/dev/null | cut -c4- | while read -r f; do [ -f "$f" ] && [ "$(stat -f %z "$f")" -lt 20000000 ] && echo "Projects/app-fabrikasi/$f"; done ) >> "$L"
find android-agent -type f -size -20000k -not -path "android-agent/web/media*" -not -path "android-agent/web/frames*" -not -path "android-agent/ytvenv/*" -not -path "*/WebDriverAgent*" -not -path "*/node_modules/*" -not -name "*.xapk" 2>/dev/null >> "$L"
find .config/parallax -type f -size -20000k -not -path "*/gemini-home/*" 2>/dev/null >> "$L"
find Projects/local-assistant/data -type f 2>/dev/null >> "$L"
find .n8n -maxdepth 2 -type f -size -20000k -not -path "*/node_modules/*" -not -name "n8nEventLog*" -not -name "database.sqlite*" 2>/dev/null >> "$L"
N=$(wc -l < "$L")
# 3) tek sifreli arsiv: dosya listesi + hazirlanan db kopyalari
OUT="$W/air-small.tar.gz.age"
( tar -czf - -T "$L" ; ) 2>>"$LOG" | age -r "$PUB" -o "$W/part1.age" || { log "HATA arsiv ya da sifreleme (1)"; exit 3; }
( cd "$W/stage" && tar -czf - . ) 2>>"$LOG" | age -r "$PUB" -o "$W/part2-db.age" || { log "HATA arsiv ya da sifreleme (db)"; exit 3; }
ok=1
upload "$W/part1.age" "air/$D/air-dosyalar.tar.gz.age" || ok=0
upload "$W/part2-db.age" "air/$D/air-veritabanlari.tar.gz.age" || ok=0
S1=$(stat -f %z "$W/part1.age"); S2=$(stat -f %z "$W/part2-db.age")
# 4) git depolari: yalniz refler degistiyse paket yukle
for r in app-fabrikasi marketing-agent; do
  P="$H/Projects/$r"; [ -d "$P/.git" ] || continue
  HASH=$(git -C "$P" for-each-ref | shasum | cut -c1-16); [ "$(cat "$CACHE/git-$r.hash" 2>/dev/null)" = "$HASH" ] && continue
  git -C "$P" bundle create "$W/$r.bundle" --all >/dev/null 2>&1 && age -r "$PUB" -o "$W/$r.bundle.age" "$W/$r.bundle" && rm -f "$W/$r.bundle" \
    && upload "$W/$r.bundle.age" "git/$r/$HASH.bundle.age" && echo "$HASH" > "$CACHE/git-$r.hash" && log "git paketi yuklendi $r $HASH $(stat -f %z "$W/$r.bundle.age") bayt" || { log "HATA git paketi $r"; ok=0; }
done
# 5) yerel temizlik: son 3 gun
ls -1d "$CACHE"/20* 2>/dev/null | sort -r | tail -n +4 | while read -r d; do rm -rf "$d"; done
rm -f "$W"/*.bundle 2>/dev/null
[ "$ok" = 1 ] && rm -f "$W"/*.age "$W/list.txt" && log "TAMAM dosya=$N dosyalar=${S1}B veritabanlari=${S2}B anahtar=air/$D/" || { log "HATA yukleme basarisiz"; exit 4; }
