#!/bin/zsh -l
# oturumlari-ac.sh : Air'deki kalici tmux oturumlarini acar (2026-10-27). LaunchAgent com.parallax.tmux-oturumlar
# Air acilinca GUI (Aqua) oturumunda calistirir; tmux sunucusu boylece GUI'nin guvenlik oturumunda baslar ve icindeki
# her surec login anahtar zincirine erisir. SSH'tan baslatilan tmux'ta codesign errSecInternalComponent veriyordu
# (anahtar zinciri "User interaction is not allowed"), claude.ai girisi de anahtar zincirinden okunur.
# Zaten acik olan oturuma dokunmaz; elle de calistirilabilir: launchctl kickstart gui/$(id -u)/com.parallax.tmux-oturumlar
T=/opt/homebrew/bin/tmux; AS="$HOME/Projects/local-assistant/bin/agent-session"  # saglayici bagimsiz acici (2026-10-28): AGENT_PROVIDER ya da agent.json
ac() { $T has-session -t "$1" 2>/dev/null && return; $T new -d -s "$1" -c "$2" "$3; exec zsh -l"; echo "$(date '+%F %T') acildi $1"; }
ac air-rc "$HOME/Projects/air-orkestrator" "AGENT_BYPASS=0 AGENT_CONTINUE=0 $AS air-orkestrator"
ac app-fabrikasi "$HOME/Projects/app-fabrikasi" "$AS app-fabrikasi"
ac marketing-agent "$HOME/Projects/marketing-agent" "zsh -l"
exit 0
