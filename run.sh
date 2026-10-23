#!/bin/bash
# Local Assistant - elle baslatma (Air'de LaunchAgent com.local-assistant.bot ayni komutu calistirir)
set -e
cd "$(dirname "$0")" || exit 1
[ -d venv ] || python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
[ -f .env ] || { echo ".env yok: cp .env.example .env ve doldur"; exit 1; }
python -m assistant.main
