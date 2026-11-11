#!/bin/bash
# log-donus.sh : Air'deki buyuyen loglari kopyala-ve-kes (copy then truncate) ile dondurur. Air'de calisir (LaunchAgent com.parallax.log-donus, gunde bir 05:30).
# Neden newsyslog degil: /etc/newsyslog.d/local-assistant.conf gecersiz R bayragi yuzunden 2026-10-04'ten beri hic calismadi, duzeltmek sudo ister.
# Neden tasima (mv) degil: loglarin cogu launchd StandardOutPath ya da python FileHandler ile acik tutuluyor; dosya tasinir ya da silinirse surec eski inode'a yazmaya devam eder, disk sizar.
# Kopyala-ve-kes dosyanin inode'unu korur; yazanlar ekleme kipinde (O_APPEND) actigi icin kesmeden sonra dosya basindan devam eder.
# Bedel: kopya ile kesme arasindaki milisaniyelerde yazilan satirlar kaybolabilir. Rehber: General App Guidlines/home-server-guvenlik.md "Log rotation".
# Kullanim: log-donus.sh [--dry-run]   Ortam: ESIK_BAYT (varsayilan 5 MB), SAKLA (varsayilan 7), KOKLER (bosluklu liste, deneme icin)
set -u
H="$HOME"; ESIK="${ESIK_BAYT:-5242880}"; SAKLA="${SAKLA:-7}"; KURU=0; [ "${1:-}" = "--dry-run" ] && KURU=1
LOG="${LOG_DONUS_LOG:-$H/android-agent/web/log-donus.log}"
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }

adaylar(){
  if [ -n "${KOKLER:-}" ]; then
    for k in $KOKLER; do find "$k" -type f \( -name "*.log" -o -name "*.err" -o -name "*.out" \) 2>/dev/null; done; return
  fi
  find "$H/Projects" -maxdepth 6 \( -name node_modules -o -name .git -o -name venv -o -name .venv -o -name __pycache__ \) -prune -o -type f \( -name "*.log" -o -name "*.err" -o -name "*.out" \) -print 2>/dev/null
  find "$H/android-agent" -maxdepth 3 \( -name WebDriverAgent -o -name ytvenv -o -name media -o -name frames -o -name node_modules -o -name venv \) -prune -o -type f \( -name "*.log" -o -name "*.err" -o -name "*.out" \) -print 2>/dev/null
  find "$H/.n8n" -maxdepth 1 -type f -name "n8n*.log" -not -name "n8nEventLog*" 2>/dev/null   # n8nEventLog dosyalarini n8n kendisi dondurur
  find "$H" -maxdepth 1 -type f -name "*.log" 2>/dev/null
  find /tmp -maxdepth 1 -type f -name "wifi-watchdog-*.log" -user "$(id -un)" 2>/dev/null
}

n=0
while IFS= read -r f; do
  [ -f "$f" ] || continue
  z=$(stat -f %z "$f" 2>/dev/null) || continue
  [ "$z" -gt "$ESIK" ] || continue
  if [ "$KURU" = 1 ]; then echo "dondurulecek $z $f"; n=$((n+1)); continue; fi
  rm -f "$f.$SAKLA.gz"
  i=$((SAKLA-1)); while [ "$i" -ge 1 ]; do [ -f "$f.$i.gz" ] && mv -f "$f.$i.gz" "$f.$((i+1)).gz"; i=$((i-1)); done
  if gzip -c "$f" > "$f.1.gz.tmp" && mv -f "$f.1.gz.tmp" "$f.1.gz"; then
    : > "$f"   # ayni inode, yazan surec dokunulmadan devam eder
    log "donduruldu $f ${z}B -> $f.1.gz $(stat -f %z "$f.1.gz")B"; n=$((n+1))
  else
    rm -f "$f.1.gz.tmp"; log "HATA sikistirma basarisiz, kesilmedi $f"
  fi
done < <(adaylar | sort -u)
[ "$KURU" = 1 ] && echo "toplam $n dosya (kuru calisma)" || log "tur bitti, $n dosya donduruldu, esik ${ESIK}B, saklanan ${SAKLA}"
