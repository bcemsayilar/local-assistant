#!/bin/zsh -l
# oturumlari-ac.sh : Air'deki kalici tmux oturumlarini acar (2026-10-27). LaunchAgent com.parallax.tmux-oturumlar
# Air acilinca GUI (Aqua) oturumunda calistirir; tmux sunucusu boylece GUI'nin guvenlik oturumunda baslar ve icindeki
# her surec login anahtar zincirine erisir. SSH'tan baslatilan tmux'ta codesign errSecInternalComponent veriyordu
# (anahtar zinciri "User interaction is not allowed"), claude.ai girisi de anahtar zincirinden okunur.
# Zaten acik olan oturuma dokunmaz; elle de calistirilabilir: launchctl kickstart gui/$(id -u)/com.parallax.tmux-oturumlar
T=/opt/homebrew/bin/tmux; C="$HOME/.local/bin/claude"
ac() { $T has-session -t "$1" 2>/dev/null && return; $T new -d -s "$1" -c "$2" "$3; exec zsh -l"; echo "$(date '+%F %T') acildi $1"; }
ac air-rc "$HOME/Projects/air-orkestrator" "env -u CLAUDE_CODE_OAUTH_TOKEN $C -n air-orkestrator --remote-control"
ac app-fabrikasi "$HOME/Projects/app-fabrikasi" "env -u CLAUDE_CODE_OAUTH_TOKEN $C -n app-fabrikasi --remote-control --dangerously-skip-permissions --continue"
ac marketing-agent "$HOME/Projects/marketing-agent" "zsh -l"
exit 0
