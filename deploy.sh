#!/bin/bash
# Build + publish the static demo to annapurna.clarifyweb.com (nginx serves /var/www/annapurna-releases/current)
set -euo pipefail
cd "$(dirname "$0")"
python3 -I tools/build.py
SHA=$(git rev-parse --short HEAD 2>/dev/null || date +%s)-$(date +%H%M%S)
DEST=/var/www/annapurna-releases/$SHA
mkdir -p "$DEST" && cp -r site/. "$DEST/"
ln -sfn "$DEST" /var/www/annapurna-releases/current
ls -1dt /var/www/annapurna-releases/*/ | tail -n +6 | xargs -r rm -rf   # keep last 5
echo "deployed $DEST"
